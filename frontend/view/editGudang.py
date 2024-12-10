import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialog
)
from backend.app import get_gudang

page = ft.Page()

def editGudang(_id: int):
    currentGudang = get_gudang(_id)
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

def getId() -> int:
    return 1

def showGudang():
    _id = getId()
    dialog = TemplateDialog(
        title=f"Gudang {_id}",
        content=editGudang(_id),
    )
    page.dialog = dialog
    dialog.open = True
    page.update()
    