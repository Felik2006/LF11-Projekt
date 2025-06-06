"""
TODO: Abhängigkeiten einfügen
 """
import sys
import traceback

from PyQt6 import uic
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QMainWindow, QPushButton, QTableView, QWidget
from utils.error_handler import show_error
from models.table_loader import init_tables
from logic.from_utils import clear_and_enable_form_fields


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tv_detail_dienstleister = self.findChild(QWidget, "tv_detail_rechnungen")
        self.tv_detail_rechnungen = self.findChild(QWidget, "tv-detail_rechnung")
        self.w_rechnung_hinzufuegen = self.findChild(QWidget, "w_rechnung_hinzufuegen")
        try:
            uic.loadUi("./Qt/main.ui", self)  # Load UI file
        except Exception as e:
            show_error("UI Loading Error", f"Could not load UI file.\nError: {str(e)}")
            sys.exit(1)

        # Database configuration
        self.db_path = "rechnungsverwaltung.db"

        # Mapping table views to database views
        self.table_mapping = {
            "tv_rechnungen": "view_invoices_full",
            "tv_dienstleister": "view_service_provider_full",
            "tv_kunden": "view_customers_full",
            "tv_positionen": "view_positions_full",
        }
        # Detail table views for specific tables
        self.detail_mapping = {
            "tv_rechnungen": self.tv_detail_rechnungen,
            "tv_dienstleister": self.tv_detail_dienstleister,
        }
        init_tables(self)

        self.w_rechnung_hinzufuegen.hide()

        # Connect the "Eintrag Hinzufügen (+)" button to clear and enable fields
        btn_hinzufuegen = self.findChild(QPushButton, "btn_eintrag_hinzufuegen")
        if btn_hinzufuegen:
            btn_hinzufuegen.clicked.connect(clear_and_enable_form_fields)


def on_row_selected(self, current: QModelIndex, db_view: str, table_view: QTableView):
    """
        Handles the event when a row is selected in a table view.
        """
    if not current.isValid():
        return

    try:
        row_id = current.sibling(current.row(), 0).data()
        print(f"Selected ID from {db_view}: {row_id}")

        # Update corresponding detail table view
        if table_view.objectName() in self.detail_mapping:
            if table_view.objectName() == "tv_rechnungen":
                self.load_invoice_positions(row_id)
            elif table_view.objectName() == "tv_dienstleister":
                self.load_service_provider_details(row_id)

        # Update textboxes and lbl_eintrag_erstellt_datum
        self.update_form_and_label(current, table_view)
    except Exception as e:
        error_message = f"Error handling row selection in {db_view}: {e}\n{traceback.format_exc()}"
        print(error_message)
        show_error("Row Selection Error", error_message)
