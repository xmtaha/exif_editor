NORDIC_STYLESHEET = """
QWidget {
    background-color: #2E3440;
    color: #ECEFF4;
    font-family: "Segoe UI", Arial, sans-serif;
}

QPushButton {
    background-color: #5E81AC;
    color: #ECEFF4;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #81A1C1;
}

QPushButton:pressed {
    background-color: #4C566A;
}

QPushButton:disabled {
    background-color: #4C566A;
    color: #9E9E9E;
}

QLabel {
    color: #ECEFF4;
}

QProgressBar {
    border: none;
    border-radius: 4px;
    background-color: #4C566A;
    text-align: center;
    color: #ECEFF4;
    height: 16px;
}

QProgressBar::chunk {
    background-color: #8FBCBB;
    border-radius: 4px;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #3B4252;
    color: #ECEFF4;
    border: 1px solid #4C566A;
    border-radius: 4px;
    padding: 4px;
}

QTextEdit:read-only, QPlainTextEdit:read-only {
    background-color: #2E3440;
    border: 1px solid #434C5E;
}

QStatusBar {
    background-color: #3B4252;
    color: #E5E9F0;
}

QScrollBar:vertical {
    border: none;
    background-color: #2E3440;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #4C566A;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #5E81AC;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #2E3440;
    height: 10px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #4C566A;
    border-radius: 5px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #5E81AC;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QGroupBox {
    border: 1px solid #4C566A;
    border-radius: 4px;
    margin-top: 12px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 3px;
}
"""

def apply_nordic_theme(app):
    app.setStyleSheet(NORDIC_STYLESHEET)