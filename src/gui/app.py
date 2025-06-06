import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from src.core.exif_processor import process_file
from src.gui.nordic_theme import apply_nordic_theme

class ProcessingWorker(QThread):
    progress_update = pyqtSignal(int, int, str, bool, str)
    processing_complete = pyqtSignal(int, int, int)
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.is_running = True
    def run(self):
        from src.core.exif_processor import scan_and_process
        def progress_callback(current, total, filepath, success, message):
            if self.is_running:
                self.progress_update.emit(current, total, filepath, success, message)
        try:
            processed, total, success, failed = scan_and_process(
                self.directory,
                progress_callback
            )
            if self.is_running:
                self.processing_complete.emit(processed, success, failed)
        except Exception as e:
            self.progress_update.emit(0, 0, "", False, f"Error processing files: {str(e)}")
            self.processing_complete.emit(0, 0, 0)
    def stop(self):
        self.is_running = False

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker = None
        self.success_count = 0
        self.failed_count = 0
    def init_ui(self):
        self.setWindowTitle("Google Photos EXIF Editor")
        self.setGeometry(100, 100, 800, 600)
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(main_widget)
        title_layout = QtWidgets.QHBoxLayout()
        logo_label = QtWidgets.QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "src", "assets", "logo.svg")
        if os.path.exists(logo_path):
            logo = QtGui.QPixmap(logo_path)
            logo_label.setPixmap(logo.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo_label.setText("📷")
            logo_label.setStyleSheet("font-size: 32px;")
        title_layout.addWidget(logo_label)
        title_text = QtWidgets.QLabel("Google Photos EXIF Editor")
        title_text.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title_text)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)
        main_layout.addSpacing(20)
        folder_group = QtWidgets.QGroupBox("Folder Selection")
        folder_layout = QtWidgets.QHBoxLayout()
        self.path_display = QtWidgets.QLineEdit()
        self.path_display.setReadOnly(True)
        self.path_display.setPlaceholderText("Select a folder to process")
        self.browse_button = QtWidgets.QPushButton("Browse...")
        self.browse_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.path_display, 7)
        folder_layout.addWidget(self.browse_button, 3)
        folder_group.setLayout(folder_layout)
        main_layout.addWidget(folder_group)
        progress_group = QtWidgets.QGroupBox("Progress")
        progress_layout = QtWidgets.QVBoxLayout()
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        file_info_layout = QtWidgets.QHBoxLayout()
        self.file_count_label = QtWidgets.QLabel("Files: 0/0")
        self.success_fail_label = QtWidgets.QLabel("Success: 0 | Failed: 0")
        file_info_layout.addWidget(self.file_count_label)
        file_info_layout.addStretch()
        file_info_layout.addWidget(self.success_fail_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addLayout(file_info_layout)
        current_file_layout = QtWidgets.QHBoxLayout()
        current_file_label_title = QtWidgets.QLabel("Current file:")
        current_file_label_title.setFixedWidth(80)
        self.current_file_label = QtWidgets.QLabel("None")
        self.current_file_label.setWordWrap(True)
        self.current_file_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        current_file_layout.addWidget(current_file_label_title)
        current_file_layout.addWidget(self.current_file_label)
        progress_layout.addLayout(current_file_layout)
        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)
        log_group = QtWidgets.QGroupBox("Log")
        log_layout = QtWidgets.QVBoxLayout()
        self.log_display = QtWidgets.QTextEdit()
        self.log_display.setReadOnly(True)
        log_layout.addWidget(self.log_display)
        log_button_layout = QtWidgets.QHBoxLayout()
        self.clear_log_button = QtWidgets.QPushButton("Clear Log")
        self.clear_log_button.clicked.connect(self.clear_log)
        log_button_layout.addStretch()
        log_button_layout.addWidget(self.clear_log_button)
        log_layout.addLayout(log_button_layout)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group, 1)
        button_layout = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton("Start Processing")
        self.start_button.clicked.connect(self.start_processing)
        self.start_button.setEnabled(False)
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_processing)
        self.stop_button.setEnabled(False)
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)
        self.setCentralWidget(main_widget)
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
    def select_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder to Process")
        if folder:
            self.path_display.setText(folder)
            self.start_button.setEnabled(True)
            self.log("Selected folder: " + folder)
    def log(self, message, level="INFO"):
        timestamp = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        color = "#ECEFF4"
        if level == "ERROR":
            color = "#BF616A"
        elif level == "SUCCESS":
            color = "#A3BE8C"
        elif level == "WARNING":
            color = "#EBCB8B"
        formatted_message = f"<span style='color:{color}'>[{timestamp}] {message}</span>"
        self.log_display.append(formatted_message)
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    def clear_log(self):
        self.log_display.clear()
    def start_processing(self):
        directory = self.path_display.text()
        if not directory:
            self.log("No folder selected", "ERROR")
            return
        self.progress_bar.setValue(0)
        self.log(f"Starting processing of directory: {directory}")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.success_count = 0
        self.failed_count = 0
        self.success_fail_label.setText(f"Success: {self.success_count} | Failed: {self.failed_count}")
        self.worker = ProcessingWorker(directory)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.processing_complete.connect(self.processing_finished)
        self.worker.start()
    def stop_processing(self):
        if self.worker and self.worker.isRunning():
            self.log("Stopping processing...", "WARNING")
            self.worker.stop()
            self.worker.wait()
            self.processing_finished()
    def update_progress(self, current, total, current_file, success, message):
        percentage = int(current / total * 100) if total > 0 else 0
        self.progress_bar.setValue(percentage)
        self.file_count_label.setText(f"Files: {current}/{total}")
        if success:
            self.success_count += 1
        else:
            self.failed_count += 1
        self.success_fail_label.setText(f"Success: {self.success_count} | Failed: {self.failed_count}")
        filename = os.path.basename(current_file)
        self.current_file_label.setText(filename)
        remaining = total - current
        self.statusBar.showMessage(f"Processing file {current} of {total} ({remaining} remaining)")
        log_level = "SUCCESS" if success else "ERROR"
        if not success or current % 10 == 0 or current == 1 or current == total:
            self.log(f"File {current}/{total}: {filename} - {message}", log_level)
    def processing_finished(self, processed=None, success=None, failed=None):
        if processed is not None and success is not None and failed is not None:
            self.log(f"Processing completed. Total: {processed}, Success: {success}, Failed: {failed}", "SUCCESS" if failed == 0 else "WARNING")
        else:
            self.log("Processing interrupted by user", "WARNING")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.statusBar.showMessage("Ready")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_nordic_theme(app)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())