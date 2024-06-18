import sys
import yaml
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListBox, QLabel, QLineEdit, QHBoxLayout, QFileDialog, QMessageBox, QTabWidget, QToolTip
from PyQt5.QtCore import Qt

class YAMLGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YAML Generator")

        # Create notebook
        self.notebook = QTabWidget()
        self.intents_tab = QWidget()
        self.entities_tab = QWidget()
        self.notebook.addTab(self.intents_tab, "Intents")
        self.notebook.addTab(self.entities_tab, "Entities")
        self.notebook.setCurrentIndex(0)

        self.create_intents_tab()
        self.create_entities_tab()

        layout = QVBoxLayout()
        layout.addWidget(self.notebook)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.show()

    def create_intents_tab(self):
        layout = QVBoxLayout()

        self.intent_listbox = QListBox()
        self.intent_add_button = QPushButton("Add Intent", self)
        self.intent_edit_button = QPushButton("Edit Intent", self)
        self.intent_delete_button = QPushButton("Delete Intent", self)

        layout.addWidget(self.intent_listbox)
        layout.addWidget(self.intent_add_button)
        layout.addWidget(self.intent_edit_button)
        layout.addWidget(self.intent_delete_button)

        self.intent_add_button.clicked.connect(self.add_intent)
        self.intent_edit_button.clicked.connect(self.edit_intent)
        self.intent_delete_button.clicked.connect(self.delete_intent)

        self.intents_tab.setLayout(layout)

    def create_entities_tab(self):
        layout = QVBoxLayout()

        self.entity_listbox = QListBox()
        self.entity_add_button = QPushButton("Add Entity", self)
        self.entity_edit_button = QPushButton("Edit Entity", self)
        self.entity_delete_button = QPushButton("Delete Entity", self)

        layout.addWidget(self.entity_listbox)
        layout.addWidget(self.entity_add_button)
        layout.addWidget(self.entity_edit_button)
        layout.addWidget(self.entity_delete_button)

        self.entity_add_button.clicked.connect(self.add_entity)
        self.entity_edit_button.clicked.connect(self.edit_entity)
        self.entity_delete_button.clicked.connect(self.delete_entity)

        self.entities_tab.setLayout(layout)

    def add_intent(self):
        intent_name, ok = QInputDialog.getText(self, "Intent Name", "Enter intent name:")
        if ok and intent_name:
            intent_data = {"type": "intent", "name": intent_name, "slots": [], "utterances": []}
            self.intents.append(intent_data)
            self.intent_listbox.addItem(intent_name)

    def edit_intent(self):
        selected_intent = self.intent_listbox.currentRow()
        if selected_intent >= 0:
            self.edit_intent_dialog(self.intents[selected_intent])

    def delete_intent(self):
        selected_intent = self.intent_listbox.currentRow()
        if selected_intent >= 0:
            del self.intents[selected_intent]
            self.intent_listbox.takeItem(selected_intent)

    def add_entity(self):
        entity_name, ok = QInputDialog.getText(self, "Entity Name", "Enter entity name:")
        if ok and entity_name:
            entity_data = {"type": "entity", "name": entity_name, "values": []}
            self.entities.append(entity_data)
            self.entity_listbox.addItem(entity_name)

    def edit_entity(self):
        selected_entity = self.entity_listbox.currentRow()
        if selected_entity >= 0:
            self.edit_entity_dialog(self.entities[selected_entity])

    def delete_entity(self):
        selected_entity = self.entity_listbox.currentRow()
        if selected_entity >= 0:
            del self.entities[selected_entity]
            self.entity_listbox.takeItem(selected_entity)

    def edit_intent_dialog(self, intent_data):
        dialog = QWidget()
        dialog.setWindowTitle("Edit Intent")

        layout = QVBoxLayout()

        name_label = QLabel("Name:")
        name_entry = QLineEdit(intent_data["name"])
        layout.addWidget(name_label)
        layout.addWidget(name_entry)

        slots_label = QLabel("Slots:")
        slots_listbox = QListBox()
        for slot in intent_data["slots"]:
            slots_listbox.addItem(f"{slot['name']}: {slot['entity']}")
        layout.addWidget(slots_label)
        layout.addWidget(slots_listbox)

        utterances_label = QLabel("Utterances:")
        utterances_listbox = QListBox()
        for utterance in intent_data["utterances"]:
            utterances_listbox.addItem(utterance)
        layout.addWidget(utterances_label)
        layout.addWidget(utterances_listbox)

        save_button = QPushButton("Save", dialog)
        save_button.clicked.connect(lambda: self.save_intent_dialog(dialog, intent_data, name_entry, slots_listbox, utterances_listbox))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def edit_entity_dialog(self, entity_data):
        dialog = QWidget()
        dialog.setWindowTitle("Edit Entity")

        layout = QVBoxLayout()

        name_label = QLabel("Name:")
        name_entry = QLineEdit(entity_data["name"])
        layout.addWidget(name_label)
        layout.addWidget(name_entry)

        values_label = QLabel("Values:")
        values_listbox = QListBox()
        for value in entity_data["values"]:
            values_listbox.addItem(value)
        layout.addWidget(values_label)
        layout.addWidget(values_listbox)

        save_button = QPushButton("Save", dialog)
        save_button.clicked.connect(lambda: self.save_entity_dialog(dialog, entity_data, name_entry, values_listbox))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_intent_dialog(self, dialog, intent_data, name_entry, slots_listbox, utterances_listbox):
        intent_data["name"] = name_entry.text()
        intent_data["slots"] = []
        for i in range(slots_listbox.count()):
            slot_name, slot_entity = slots_listbox.item(i).text().split(": ")
            intent_data["slots"].append({"name": slot_name, "entity": slot_entity})
        intent_data["utterances"] = []
        for i in range(utterances_listbox.count()):
            intent_data["utterances"].append(utterances_listbox.item(i).text())
        dialog.close()

    def save_entity_dialog(self, dialog, entity_data, name_entry, values_listbox):
        entity_data["name"] = name_entry.text()
        entity_data["values"] = []
        for i in range(values_listbox.count()):
            entity_data["values"].append(values_listbox.item(i).text())
        dialog.close()

    def save_to_yaml(self):
        yaml_data = []
        for intent in self.intents:
            yaml_data.append(intent)
        for entity in self.entities:
            yaml_data.append(entity)

        file_path, _ = QFileDialog.getSaveFileName(self, "Save YAML file", "", "YAML files (*.yaml)")
        if file_path:
            with open(file_path, "w") as f:
                yaml.dump(yaml_data, f, default_flow_style=False)
            QMessageBox.information(self, "Success", "YAML file saved successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    generator = YAMLGenerator()
    generator.save_button = QPushButton("Save to YAML", generator)
    generator.save_button.clicked.connect(generator.save_to_yaml)
    generator.layout().addWidget(generator.save_button)
    sys.exit(app.exec_())