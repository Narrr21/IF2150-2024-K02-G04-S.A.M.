import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialogTextField, TemplateDialog,
    TemplateCard, TemplateIconButton
)
from frontend.const import DARK_TEXT, TURQUOISE
from backend.app import get_all_gudang, get_gudang, update_gudang, delete_gudang, create_gudang, Gudang, get_gudang_by_name, get_barang_by_name, pindah_barang
from frontend.view.barangPage import barangPage


def moveBarangOverlay(page: ft.Page, gudang_page):
    def close_dlg(e):
        dlg.open = False
        page.update()

    def save_changes(e):
        # Implement save changes logic here
        name_source = dlg.fields[0].value
        name_destination = dlg.fields[1].value
        name_barang = dlg.fields[2].value
        qty = dlg.fields[3].value

        if (get_gudang_by_name(name_source) is None) or (get_gudang_by_name(name_destination) is None) or (get_barang_by_name(name_barang) is None):
            dlg.fields[0].error_text = "Gudang or Barang not found"
            dlg.fields[0].border_color = "red"
            dlg.fields[0].update()

        barangs = get_barang_by_name(name_barang)
        id_barang = barangs._id
        id_gudang_source = get_gudang_by_name(name_source)._id
        id_gudang_destination = get_gudang_by_name(name_destination)._id
        qty_barang_in_source = 0
        barang_is_in = False
        for barang in get_gudang(id_gudang_source).list_barang:
            if barang[0] == id_barang:
                qty_barang_in_source = barang[1]
                barang_is_in = True
                break
        if not barang_is_in:
            dlg.fields[2].error_text = "Barang not found in source gudang"
            dlg.fields[2].border_color = "red"
            dlg.fields[2].update()
            return
        if int(qty) > qty_barang_in_source:
            dlg.fields[3].error_text = "Quantity exceeds the available quantity in source gudang"
            dlg.fields[3].border_color = "red"
            dlg.fields[3].update()
            return

        curr_capacity, max_capacity = get_gudang(id_gudang_destination).capacity, get_gudang(id_gudang_destination).max_capacity
        if curr_capacity + int(qty)*barangs.capacity > max_capacity:
            dlg.fields[1].error_text = "Destination gudang don't have enough space!"
            dlg.fields[1].border_color = "red"
            dlg.fields[1].update()
            return
        
        
            
        gudang_source = get_gudang_by_name(name_source)
        gudang_destination = get_gudang_by_name(name_destination)
        barang_move = get_barang_by_name(name_barang)
        pindah_barang(barang_move._id, gudang_source._id, gudang_destination._id, int(qty))
        dlg.open = False

        gudang_page.refreshScreen()
        page.update()
        
    dlg = TemplateDialogTextField(
        title="Move Barang",
        fields=[
            TemplateTextField(
                label="Gudang Source",
                hint_text="Enter the name of the gudang source",
                width=300,
                autofocus=True
            ),
            TemplateTextField(
                label="Gudang Destination",
                hint_text="Enter the name of the gudang destination",
                width=300
            ),
            TemplateTextField(
                label="Barang Name",
                hint_text="Enter the name of the barang",
                width=300
            ),
            TemplateTextField(
                label="Quantity",
                hint_text="Enter the quantity of barang",
                width=300
            ),
        ],
        actions=[
            TemplateButton(
                text="Move Barang",
                style="primary",
                on_click=save_changes
            ),
            TemplateButton(
                text="Close",
                style="secondary",
                on_click=close_dlg
            ),
        ]
    )
    dlg.content = ft.Column(dlg.fields, height=230)
    page.overlay.append(dlg)
    dlg.open = True
    page.update()


def deleteGudangOverlay(page: ft.Page, id: int, gudang_page):
    def close_dlg(e):
        dlg.open = False
        page.update()

    def confirm_delete(e):
        delete_gudang(id)
        gudang_page.refreshScreen()
        page.close_dialog()

    dlg = TemplateDialog(
        title="Confirm Delete",
        content="Are you sure you want to delete this gudang?",
        actions=[
            TemplateButton(
                text="Yes",
                style="primary",
                on_click=confirm_delete
            ),
            TemplateButton(
                text="No",
                style="secondary",
                on_click=close_dlg
            ),
        ]
    )
    page.show_dialog(dlg)

def editGudangOverlay(page: ft.Page, id: int, gudang_page):
    def close_dlg(e):
        dlg.open = False
        page.update()

    def validate_input_name(e):
        gudang_name_field = dlg.fields[0]
        gudang_name_field.error_text = None
        gudang_name_field.border_color = None

        if len(gudang_name_field.value) > 30:
            gudang_name_field.error_text = "Maximum 30 Characters"
            gudang_name_field.border_color = "red"
            gudang_name_field.update()
            return
        else:
            gudang_name_field.error_text = None
            gudang_name_field.border_color = None
            gudang_name_field.update()
            return


    def validate_input_capacity(e):
        updated_max_capacity = dlg.fields[1]
        updated_max_capacity.error_text = None
        updated_max_capacity.border_color = None

        if updated_max_capacity.value == "":
            updated_max_capacity.error_text = None
            updated_max_capacity.border_color = None
            updated_max_capacity.update()
            return
        try:
            max_capacity = int(updated_max_capacity.value)
        except ValueError:
            updated_max_capacity.error_text = "Input must be a number"
            updated_max_capacity.border_color = "red"
            updated_max_capacity.update()
        else:
            if max_capacity <= 0:
                updated_max_capacity.error_text = "Input must be greater than 0"
                updated_max_capacity.border_color = "red"
        updated_max_capacity.update()

    def save_changes(e):
        updated_name = dlg.fields[0].value
        updated_max_capacity_field = dlg.fields[1]

        if updated_max_capacity_field.value == "":
            updated_max_capacity_field.error_text = None
            updated_max_capacity_field.border_color = None
            updated_max_capacity_field.update()
            updated_max_capacity = -1
        else: 
            try:
                updated_max_capacity = int(updated_max_capacity_field.value)
            except ValueError:
                updated_max_capacity_field.error_text = "Input must be a number"
                updated_max_capacity_field.border_color = "red"
                updated_max_capacity_field.update()
                return
            
            if updated_max_capacity <= 0:
                updated_max_capacity_field.error_text = "Input must be greater than 0"
                updated_max_capacity_field.border_color = "red"
                updated_max_capacity_field.update()
                return
        
        if updated_name:
            gudang.gudang_name = updated_name
        if updated_max_capacity > 0:    
            gudang.max_capacity = updated_max_capacity
        update_gudang(gudang)
        gudang_page.refreshScreen()
        page.close_dialog()

    gudang = get_gudang(id)
    dlg = TemplateDialogTextField(
        title="Edit Gudang",
        fields=[
            TemplateTextField(
                label="Gudang Name",
                hint_text="Enter Gudang Name",
                width=300,
                autofocus=True,
                on_change=validate_input_name
            ),
            TemplateTextField(
                label="Max Capacity",
                hint_text="Enter Max Capacity",
                width=300,
                on_change=validate_input_capacity
            ),
        ],
        actions=[
            TemplateButton(
                text="Save Changes",
                style="primary",
                on_click=save_changes
            ),
            TemplateButton(
                text="Cancel",
                style="secondary",
                on_click=close_dlg
            ),
        ]
    )

    page.show_dialog(dlg)

def createGudangOverlay(page: ft.Page, gudang_page):
    def close_dlg(e):
        page.close_dialog()

    def validate_input_name(e):
        gudang_name_field = dlg.fields[0]
        gudang_name_field.error_text = None
        gudang_name_field.border_color = None

        if len(gudang_name_field.value) > 30:
            gudang_name_field.error_text = "Maximum 30 Characters"
            gudang_name_field.border_color = "red"
            gudang_name_field.update()
            return
        else:
            gudang_name_field.error_text = None
            gudang_name_field.border_color = None
            gudang_name_field.update()
            return


    def validate_input_capacity(e):
        max_capacity_field = dlg.fields[1]
        max_capacity_field.error_text = None
        max_capacity_field.border_color = None

        if max_capacity_field.value == "":
            max_capacity_field.error_text = None
            max_capacity_field.border_color = None
            max_capacity_field.update()
            return
        try:
            max_capacity = int(max_capacity_field.value)
        except ValueError:
            max_capacity_field.error_text = "Must be a number"
            max_capacity_field.border_color = "red"
            max_capacity_field.update()
        else:
            if max_capacity <= 0:
                max_capacity_field.error_text = "Must be greater than 0"
                max_capacity_field.border_color = "red"
        max_capacity_field.update()

    def create_gudangs(e):
        gudang_name = dlg.fields[0].value
        max_capacity_field = dlg.fields[1]
        if gudang_name == "":
            dlg.fields[0].error_text = "Name cannot be empty"
            dlg.fields[0].border_color = "red"
            dlg.fields[0].update()
            return  
        
        if not max_capacity_field.value:
            max_capacity_field.error_text = "Capacity cannot be empty"
            max_capacity_field.border_color = "red"
            max_capacity_field.update()
            return

        try:
            max_capacity = int(max_capacity_field.value)
        except ValueError:
            max_capacity_field.error_text = "Must be a number"
            max_capacity_field.border_color = "red"
            max_capacity_field.update()
            return
        
        if max_capacity <= 0:
            max_capacity_field.error_text = "Must be greater than 0"
            max_capacity_field.border_color = "red"
            max_capacity_field.update()
            return
        
        gudang = Gudang(gudang_name, 0, max_capacity, [])
        create_gudang(gudang)
        gudang_page.refreshScreen()
        page.close_dialog()
        

    dlg = TemplateDialogTextField(
        title="Create Gudang",
        fields=[
            TemplateTextField(
                label="Gudang Name",
                hint_text="Enter Gudang Name",
                width=300,
                autofocus=True,
                on_change=validate_input_name
            ),
            TemplateTextField(
                label="Max Capacity",
                hint_text="Enter Max Capacity",
                width=300,
                autofocus=True,
                on_change=validate_input_capacity
            ),
        ],
        actions=[
            TemplateButton(
                text="Create Gudang",
                style="primary",
                on_click=create_gudangs
            ),
            TemplateButton(
                text="Cancel",
                style="secondary",
                on_click=close_dlg
            ),
        ]
    )

    page.show_dialog(dlg)

class gudangPage(ft.UserControl):
    # Initialize page with template
    def __init__(self, page: ft.Page, content_area: ft.Container):
        super().__init__()
        self.page = page
        self.content_area = content_area
    
    def switchToBarangPage(self, gudang_id):
        barang_page = barangPage(self.page, gudang_id).build()
        self.content_area.clean()
        self.content_area.content = barang_page
        self.content_area.update()

    def refreshScreen(self):
        self.content_area.clean()
        self.content_area.content = self.build()
        self.content_area.update()

    def build(self):
        page = self.page
        ListGudang = get_all_gudang()

        gudang_cards = [
        TemplateCard(
            title=Gudang.gudang_name,
            content=ft.Column([
                ft.Divider(),
                ft.Container(
                    content=ft.Text(
                    f"CAPACITY: {Gudang.capacity}/{Gudang.max_capacity}",
                    text_align=ft.TextAlign.CENTER
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                ),
                ft.Container(
                    content=ft.Text(
                    "FULL!" if Gudang.capacity == Gudang.max_capacity else "Available",
                    color="red" if Gudang.capacity == Gudang.max_capacity else "green",
                    text_align=ft.TextAlign.CENTER
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                ),
                ft.Divider(height=8, color="transparent"),
                ft.Row([
                    TemplateIconButton(
                        icon=ft.icons.EDIT_OUTLINED,
                        icon_color=TURQUOISE,
                        on_click=lambda e, gudang_id=Gudang._id: (
                            editGudangOverlay(page, gudang_id, self)
                        )
                    ),
                    TemplateIconButton(
                        icon=ft.icons.DELETE_OUTLINE,
                        icon_color=ft.colors.RED,
                        on_click=lambda e, gudang_id=Gudang._id: (
                            deleteGudangOverlay(page, gudang_id, self)
                        )
                    )
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=15, color="transparent"),
                ft.Row(
                    [TemplateButton(
                        text="Enter",
                        style="outline",
                        width=200,
                        on_click=lambda e, gudang_id=Gudang._id: self.switchToBarangPage(gudang_id)
                    )],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
        )
        for Gudang in ListGudang
        ]
        gudang_cards.append(
            TemplateCard(
                title="Create Gudang",
                content=ft.Column([
                    ft.Divider(),
                    ft.Container(
                        content=ft.Icon(ft.icons.ADD, size=50, color=TURQUOISE),
                        alignment=ft.alignment.center,
                        expand=True
                    ),
                    ft.Divider(height=8, color="transparent"),
                    ft.Row([
                        TemplateButton(
                            text="Create Gudang",
                            style="outline",
                            width=200,
                            on_click=lambda e: createGudangOverlay(page, self)
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
            )
        )

        grid_view = ft.GridView(
            expand=True,
            max_extent=300,
            spacing=10,
            run_spacing=10,
            padding=20,
            controls=gudang_cards
        )
        
        return grid_view
    
