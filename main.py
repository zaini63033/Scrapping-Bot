import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QDateEdit, QSpinBox, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QDate
import init  # Import the refactored input.py

class DateTabInputApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Inheritance List')

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.start_date_input = QDateEdit()
        self.start_date_input.setDisplayFormat("MM/dd/yyyy")
        self.start_date_input.setMinimumSize(300, 50)
        self.start_date_input.setStyleSheet("font-size: 18px; padding: 5px;")
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)

        self.end_date_input = QDateEdit()
        self.end_date_input.setDisplayFormat("MM/dd/yyyy")
        self.end_date_input.setMinimumSize(300, 50)
        self.end_date_input.setStyleSheet("font-size: 18px; padding: 5px;")
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)

        self.num_tabs_input = QSpinBox()
        self.num_tabs_input.setMinimumSize(300, 50)
        self.num_tabs_input.setStyleSheet("font-size: 18px; padding: 5px;")
        self.num_tabs_input.setRange(1, 10000)
        self.num_tabs_input.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)

        self.path_button = QPushButton("Select Save Path")
        self.path_button.setMinimumSize(300, 50)
        self.path_button.setStyleSheet(
            "font-size: 18px; padding: 5px; background: transparent; border: 2px solid black; text-align: left;"
        )
        self.path_button.clicked.connect(self.openFileDialog)
        self.save_path = ""

        start_date_label = QLabel('Start Date:')
        start_date_label.setStyleSheet("font-size: 18px; text-align: center;")
        form_layout.addRow(start_date_label, self.start_date_input)

        end_date_label = QLabel('End Date:')
        end_date_label.setStyleSheet("font-size: 18px; text-align: center;")
        form_layout.addRow(end_date_label, self.end_date_input)

        num_tabs_label = QLabel('Tabs:')
        num_tabs_label.setStyleSheet("font-size: 18px; text-align: center;")
        form_layout.addRow(num_tabs_label, self.num_tabs_input)

        path_label = QLabel('Save Path:')
        path_label.setStyleSheet("font-size: 18px; text-align: center;")
        form_layout.addRow(path_label, self.path_button)

        submit_button = QPushButton('Submit')
        submit_button.setMinimumSize(150, 50)
        submit_button.setStyleSheet("font-size: 18px;")
        submit_button.clicked.connect(self.run_init_script)
        form_layout.addRow(submit_button)

        main_layout.addStretch()
        main_layout.addLayout(form_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.resize(600, 500)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.show()

    def openFileDialog(self):
        options = QFileDialog.Option.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", "", options=options)
        if directory:
            self.path_button.setText(directory)
            self.save_path = directory

    def run_init_script(self):
        start_date = self.start_date_input.date().toString("MM/dd/yyyy")
        end_date = self.end_date_input.date().toString("MM/dd/yyyy")
        tabs = self.num_tabs_input.value()
        save_path = self.save_path

        init.run_scraping_bot(tabs, start_date, end_date, save_path)

# Run the application
app = QApplication(sys.argv)
window = DateTabInputApp()
sys.exit(app.exec())
