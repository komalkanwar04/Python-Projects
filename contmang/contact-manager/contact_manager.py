import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QInputDialog, QFormLayout, QDialog
)
from PyQt5.QtCore import Qt

CONTACTS_FILE = "contacts.json"

class ContactDialog(QDialog):
    def __init__(self, parent=None, contact=None):
        super().__init__(parent)
        self.setWindowTitle("Contact Details")
        self.contact = contact or {"name": "", "phone": "", "email": "", "address": ""}
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        self.name_edit = QLineEdit(self.contact["name"])
        self.phone_edit = QLineEdit(self.contact["phone"])
        self.email_edit = QLineEdit(self.contact["email"])
        self.address_edit = QLineEdit(self.contact["address"])

        layout.addRow("Name:", self.name_edit)
        layout.addRow("Phone:", self.phone_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("Address:", self.address_edit)

        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addRow(buttons_layout)

    def get_contact_data(self):
        return {
            "name": self.name_edit.text().strip(),
            "phone": self.phone_edit.text().strip(),
            "email": self.email_edit.text().strip(),
            "address": self.address_edit.text().strip()
        }

class ContactManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Manager")
        self.contacts = []
        self.load_contacts()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #ffffff;")  # Medium tone background for main window

        main_layout = QVBoxLayout(self)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_edit = QLineEdit()
        self.search_edit.setStyleSheet("background-color: #c0c0c0;")  # Medium tone background for input
        self.search_edit.textChanged.connect(self.update_contact_list)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        main_layout.addLayout(search_layout)

        # Contact list
        self.contact_list = QListWidget()
        self.contact_list.setStyleSheet("background-color: #c0c0c0;")  # Medium tone background for list
        self.contact_list.itemSelectionChanged.connect(self.on_contact_selected)
        main_layout.addWidget(self.contact_list)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Contact")
        self.add_button.setStyleSheet("background-color: #198450;")  # Medium tone buttons
        self.add_button.clicked.connect(self.add_contact)
        self.update_button = QPushButton("Update Contact")
        self.update_button.setStyleSheet("background-color: #0747a1;")
        self.update_button.clicked.connect(self.update_contact)
        self.delete_button = QPushButton("Delete Contact")
        self.delete_button.setStyleSheet("background-color: #960018;")
        self.delete_button.clicked.connect(self.delete_contact)
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.update_button)
        buttons_layout.addWidget(self.delete_button)
        main_layout.addLayout(buttons_layout)

        self.selected_index = None
        self.update_contact_list()

    def load_contacts(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r") as f:
                self.contacts = json.load(f)
        else:
            self.contacts = []

    def save_contacts(self):
        with open(CONTACTS_FILE, "w") as f:
            json.dump(self.contacts, f, indent=4)

    def update_contact_list(self):
        search_term = self.search_edit.text().lower()
        self.contact_list.clear()
        for i, contact in enumerate(self.contacts):
            if search_term in contact["name"].lower() or search_term in contact["phone"]:
                self.contact_list.addItem(f"{contact['name']} - {contact['phone']}")

    def on_contact_selected(self):
        selected_items = self.contact_list.selectedItems()
        if selected_items:
            self.selected_index = self.contact_list.currentRow()
        else:
            self.selected_index = None

    def add_contact(self):
        dialog = ContactDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_contact = dialog.get_contact_data()
            if not new_contact["name"] or not new_contact["phone"]:
                QMessageBox.warning(self, "Input Error", "Name and Phone are required.")
                return
            self.contacts.append(new_contact)
            self.save_contacts()
            self.update_contact_list()

    def update_contact(self):
        if self.selected_index is None:
            QMessageBox.warning(self, "Selection Error", "No contact selected.")
            return
        dialog = ContactDialog(self, self.contacts[self.selected_index])
        if dialog.exec_() == QDialog.Accepted:
            updated_contact = dialog.get_contact_data()
            if not updated_contact["name"] or not updated_contact["phone"]:
                QMessageBox.warning(self, "Input Error", "Name and Phone are required.")
                return
            self.contacts[self.selected_index] = updated_contact
            self.save_contacts()
            self.update_contact_list()

    def delete_contact(self):
        if self.selected_index is None:
            QMessageBox.warning(self, "Selection Error", "No contact selected.")
            return
        reply = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this contact?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            del self.contacts[self.selected_index]
            self.save_contacts()
            self.update_contact_list()
            self.selected_index = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactManager()
    window.resize(400, 500)
    window.show()
    sys.exit(app.exec_())
