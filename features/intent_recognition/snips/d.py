import sys
import yaml
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit, QMessageBox, QTabWidget, QInputDialog, QCheckBox


class YAMLGenerator(QWidget):
    save_button = None
    intents = []
    entities = []
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

        self.setLayout(layout)

        self.show()

    def create_intents_tab(self):
        layout = QVBoxLayout()

        self.intent_listbox = QListWidget()
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

        self.entity_listbox = QListWidget()
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

    def add_slot(self, slots_listbox):
        slot_name, ok = QInputDialog.getText(self, "Slot Name", "Enter slot name:")
        if ok and slot_name:
            slot_entity, ok = QInputDialog.getText(self, "Slot Entity", "Enter slot entity:")
            if ok and slot_entity:
                slots_listbox.addItem(f"{slot_name}: {slot_entity}")

    def remove_slot(self, slots_listbox):
        selected_slot = slots_listbox.currentRow()
        if selected_slot >= 0:
            slots_listbox.takeItem(selected_slot)

    def add_utterance(self, utterances_listbox):
        utterance, ok = QInputDialog.getText(self, "Utterance", "Enter utterance:")
        if ok and utterance:
            utterances_listbox.addItem(utterance)

    def remove_utterance(self, utterances_listbox):
        selected_utterance = utterances_listbox.currentRow()
        if selected_utterance >= 0:
            utterances_listbox.takeItem(selected_utterance)


    def edit_intent_dialog(self, intent_data):
        dialog = QWidget()
        dialog.setWindowTitle("Edit Intent")

        layout = QVBoxLayout()

        name_label = QLabel("Name:")
        name_entry = QLineEdit(intent_data["name"])
        layout.addWidget(name_label)
        layout.addWidget(name_entry)

        slots_label = QLabel("Slots:")
        slots_listbox = QListWidget()
        for slot in intent_data["slots"]:
            slots_listbox.addItem(f"{slot['name']}: {slot['entity']}")
        layout.addWidget(slots_label)
        layout.addWidget(slots_listbox)

        add_slot_button = QPushButton("Add Slot", dialog)
        add_slot_button.clicked.connect(lambda: self.add_slot(slots_listbox))
        layout.addWidget(add_slot_button)

        remove_slot_button = QPushButton("Remove Slot", dialog)
        remove_slot_button.clicked.connect(lambda: self.remove_slot(slots_listbox))
        layout.addWidget(remove_slot_button)

        utterances_label = QLabel("Utterances:")
        utterances_listbox = QListWidget()
        for utterance in intent_data["utterances"]:
            utterances_listbox.addItem(utterance)
        layout.addWidget(utterances_label)
        layout.addWidget(utterances_listbox)
        
        add_utterance_button = QPushButton("Add Utterance", dialog)
        add_utterance_button.clicked.connect(lambda: self.add_utterance(utterances_listbox))
        layout.addWidget(add_utterance_button)

        remove_utterance_button = QPushButton("Remove Utterance", dialog)
        remove_utterance_button.clicked.connect(lambda: self.remove_utterance(utterances_listbox))
        layout.addWidget(remove_utterance_button)

        save_button = QPushButton("Save", dialog)
        save_button.clicked.connect(lambda: self.save_intent_dialog(dialog, intent_data, name_entry, slots_listbox, utterances_listbox))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.show()

    def edit_entity_dialog(self, entity_data):
        dialog = QWidget()
        dialog.setWindowTitle("Edit Entity")

        layout = QVBoxLayout()

        type_label = QLabel("Type:")
        type_entry = QLineEdit(entity_data["type"])
        layout.addWidget(type_label)
        layout.addWidget(type_entry)

        name_label = QLabel("Name:")
        name_entry = QLineEdit(entity_data["name"])
        layout.addWidget(name_label)
        layout.addWidget(name_entry)

        automatically_extensible_label = QLabel("Automatically Extensible:")
        automatically_extensible_checkbox = QCheckBox()
        automatically_extensible_checkbox.setChecked(not entity_data.get("automatically_extensible", True))
        layout.addWidget(automatically_extensible_label)
        layout.addWidget(automatically_extensible_checkbox)

        use_synonyms_label = QLabel("Use Synonyms:")
        use_synonyms_checkbox = QCheckBox()
        use_synonyms_checkbox.setChecked(entity_data.get("use_synonyms", True))
        layout.addWidget(use_synonyms_label)
        layout.addWidget(use_synonyms_checkbox)

        matching_strictness_label = QLabel("Matching Strictness:")
        matching_strictness_entry = QLineEdit(str(entity_data.get("matching_strictness", 1.0)))
        layout.addWidget(matching_strictness_label)
        layout.addWidget(matching_strictness_entry)

        values_label = QLabel("Values:")
        values_listbox = QListWidget()
        for value in entity_data["values"]:
            if isinstance(value, list):
                values_listbox.addItem(", ".join(value))
            else:
                values_listbox.addItem(value)
        layout.addWidget(values_label)
        layout.addWidget(values_listbox)

        add_value_button = QPushButton("Add Value", dialog)
        add_value_button.clicked.connect(lambda: self.add_value(values_listbox))
        layout.addWidget(add_value_button)

        remove_value_button = QPushButton("Remove Value", dialog)
        remove_value_button.clicked.connect(lambda: self.remove_value(values_listbox))
        layout.addWidget(remove_value_button)

        save_button = QPushButton("Save", dialog)
        save_button.clicked.connect(lambda: self.save_entity_dialog(dialog, entity_data, type_entry, name_entry, automatically_extensible_checkbox, use_synonyms_checkbox, matching_strictness_entry, values_listbox))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.show()

    def add_value(self, values_listbox):
        value, ok = QInputDialog.getText(self, "Value", "Enter value:")
        if ok and value:
            values_listbox.addItem(value)

    def remove_value(self, values_listbox):
        selected_value = values_listbox.currentRow()
        if selected_value >= 0:
            values_listbox.takeItem(selected_value)

    def save_entity_dialog(self, dialog, entity_data, type_entry, name_entry, automatically_extensible_checkbox, use_synonyms_checkbox, matching_strictness_entry, values_listbox):
        entity_data["type"] = type_entry.text()
        entity_data["name"] = name_entry.text()
        entity_data["automatically_extensible"] = not automatically_extensible_checkbox.isChecked()
        entity_data["use_synonyms"] = use_synonyms_checkbox.isChecked()
        entity_data["matching_strictness"] = float(matching_strictness_entry.text())
        entity_data["values"] = []
        for i in range(values_listbox.count()):
            value = values_listbox.item(i).text()
            if ", " in value:
                entity_data["values"].append([x.strip() for x in value.split(", ")])
            else:
                entity_data["values"].append(value)
        dialog.close()

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

    def save_to_yaml(self):
        data = []
        for intent in self.intents:
            intent_data = {
                "type": "intent",
                "name": intent["name"],
                "slots": intent["slots"],
                "utterances": intent["utterances"]
            }
            data.append(intent_data)
        for entity in self.entities:
            entity_data = {
                "type": "entity",
                "name": entity["name"],
                "automatically_extensible": entity.get("automatically_extensible", True),
                "use_synonyms": entity.get("use_synonyms", True),
                "matching_strictness": entity.get("matching_strictness", 1.0),
                "values": entity["values"]
            }
            data.append(entity_data)

        with open("data.yaml", "w") as f:
            yaml.dump(data, f, default_flow_style=False)
        QMessageBox.information(self, "Success", "YAML file saved successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    generator = YAMLGenerator()
    generator.save_button = QPushButton("Save to YAML", generator)
    generator.save_button.clicked.connect(generator.save_to_yaml)
    generator.layout().addWidget(generator.save_button)
    sys.exit(app.exec_())