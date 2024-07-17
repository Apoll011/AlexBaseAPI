import sys
from PyQt5.QtWidgets import  QSpacerItem, QApplication, QMainWindow, QTabWidget, QListWidget, QListWidgetItem, QLineEdit, QFormLayout, QLabel, QCheckBox, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QInputDialog
from PyQt5.QtCore import Qt

class IntentEntityTab(QTabWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        layout.addSpacing(10)
        self.element_list = ElementList()
        layout.addWidget(self.element_list)

        self.search_bar = QLineEdit()
        layout.addWidget(self.search_bar)
        
        self.addTab(QWidget(), "Intents")
        self.addTab(QWidget(), "Entities")
        self.setLayout(layout)

class ElementList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(250)
        self.setMaximumWidth(250)

class EntityElementForm(QWidget):
    def __init__(self):
        super().__init__()
        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)

        self.name_label = QLabel("Name:")
        self.name_field = QLineEdit()
        self.form_layout.addRow(self.name_label, self.name_field)

        self.automatically_extensible = QCheckBox("Automatically Extensible")
        self.form_layout.addWidget(self.automatically_extensible)

        self.use_synonyms = QCheckBox("Use Synonyms")
        self.form_layout.addWidget(self.use_synonyms)

        self.matching_strictness_label = QLabel("Matching Strictness:")
        self.matching_strictness = QSpinBox()
        self.form_layout.addRow(self.matching_strictness_label, self.matching_strictness)

        self.list_label = QLabel("Values:")
        self.list_widget = QListWidget()
        self.form_layout.addRow(self.list_label, self.list_widget)

        self.plus_button = QPushButton("+")
        self.plus_button.clicked.connect(self.addToList)
        self.form_layout.addWidget(self.plus_button)

        self.save_button = QPushButton("Save")
        self.form_layout.addWidget(self.save_button)

    def addToList(self):
        text, ok = QInputDialog.getText(self, "Add to List", "Enter text:")
        if ok:
            self.list_widget.addItem(text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Intent App")
        self.setGeometry(300, 300, 800, 600)

        self.top_bar = IntentEntityTab()

        self.top_bar.element_list.addItems(["fea", "Fsdds", "DSgfsdf", "DSfgsdf", "DSgfsdg"," gsd"])

        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_widget.setLayout(self.left_layout)
        self.left_layout.addWidget(self.top_bar)

        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_widget.setLayout(self.right_layout)

        self.element_form = EntityElementForm()
        self.right_layout.addWidget(self.element_form)

        self.central_widget = QWidget()
        self.central_layout = QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        self.central_layout.addWidget(self.left_widget)
        self.central_layout.addWidget(self.right_widget)

        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())