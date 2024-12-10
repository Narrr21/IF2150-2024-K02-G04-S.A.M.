import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialog
)
from backend.controller.gudangManager import GudangManager
from backend.app import get_gudang

def editGudang(id):
    print("Edit Gudang")

class EditGudangPage(ft.UserControl):  
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.gudang_manager = GudangManager()

    def showEditGudang(self):
        currentGudang = get_gudang(self.id)
        return ft.Column([
            ft.Text("Nama Gudang", size=20, weight="bold"),
            TemplateTextField(
                label={currentGudang.gudang_name},
                hint_text="Masukan nama gudang baru"
            ),
            ft.Text("Max Capacity Gudang", size=20, weight="bold"),
            TemplateTextField(
                label={currentGudang.max_capacity},
                hint_text="Masukan max capacity baru"
            ),
            TemplateButton(
                text="Save",
                on_click=lambda _: editGudang(1)
            )
        ])
    