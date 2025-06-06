import os
import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    
    try:
        from src.gui.app import MainApp
        from src.gui.nordic_theme import apply_nordic_theme
        app = QApplication(sys.argv)
        apply_nordic_theme(app)
        window = MainApp()
        window.show()
        window.log(f"Application started successfully")
        window.log(f"Base directory: {base_dir}")
        sys.exit(app.exec_())
    except Exception as e:
        error_message = f"An error occurred during application startup:\n{str(e)}\n\n{traceback.format_exc()}"
        try:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Startup Error")
            msg_box.setText("The application failed to start.")
            msg_box.setDetailedText(error_message)
            msg_box.exec_()
        except:
            print(error_message)
        sys.exit(1)

if __name__ == "__main__":
    main()