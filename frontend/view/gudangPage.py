import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialogTextField, TemplateDialog,
    TemplateCard, TemplateListItem, TemplatePage,
    TemplateAppBar, TemplateNavigationRail, TemplateIconButton
)
from frontend.const import DARK_TEXT, TURQUOISE
from backend.app import get_all_gudang, get_gudang, update_gudang, delete_gudang
from frontend.view.barangPage import barangPage

def deleteGudangOverlay(page: ft.Page, id: int):
    def close_dlg(e):
        dlg.open = False
        page.update()

    def confirm_delete(e):
        delete_gudang(id)
        dlg.open = False
        page.clean()
        gudangPage(page)
        page.update()

    dlg = TemplateDialog(
        title="Confirm Delete",
        content=ft.Text("Are you sure you want to delete this gudang?"),
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

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def editGudangOverlay(page: ft.Page, id: int):
    def close_dlg(e):
        dlg.open = False
        page.update()

    def save_changes(e):
        # Implement save changes logic here
        updated_name = dlg.fields[0].value
        updated_max_capacity = dlg.fields[1].value
        if updated_name:
            gudang.name = updated_name
        if updated_max_capacity:    
            gudang.max_capacity = updated_max_capacity
        dlg.open = False
        update_gudang(gudang)
        page.clean()
        gudangPage(page)
        page.update()

    gudang = get_gudang(id)
    dlg = TemplateDialogTextField(
        title="Edit Gudang",
        fields=[
            TemplateTextField(
                label="Gudang Name",
                hint_text="Masukkan nama gudang",
                width=300,
                autofocus=True
            ),
            TemplateTextField(
                label="Max Capacity",
                hint_text="Masukkan max capacity",
                width=300
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

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def createGudangOverlay(page: ft.Page):
    def close_dlg(e):
        dlg.open = False
        page.update()

    def create_gudang(e):
        # Implement create gudang logic here
        gudang_name = dlg.fields[0].value
        capacity = dlg.fields[1].value
        max_capacity = dlg.fields[2].value
        if gudang_name and capacity and max_capacity:
            create_gudang(gudang_name, capacity, max_capacity, [])
        dlg.open = False
        page.clean()
        gudangPage(page)
        page.update()
        

    dlg = TemplateDialogTextField(
        title="Create Gudang",
        fields=[
            TemplateTextField(
                label="Gudang Name",
                hint_text="Masukkan nama gudang",
                width=300,
                autofocus=True
            ),
            TemplateTextField(
                label="Max Capacity",
                hint_text="Masukkan max capacity",
                width=300
            ),
        ],
        actions=[
            TemplateButton(
                text="Create Gudang",
                style="primary",
                on_click=create_gudang
            ),
            TemplateButton(
                text="Cancel",
                style="secondary",
                on_click=close_dlg
            ),
        ]
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def gudangPage(page: ft.Page) -> int:
    # Initialize page with template
    page.__class__ = TemplatePage
    page.title = "Storage Allocation Manager"

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
                        editGudangOverlay(page, gudang_id)
                    )
                ),
                TemplateIconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color=ft.colors.RED,
                    on_click=lambda e, gudang_id=Gudang._id: (
                        deleteGudangOverlay(page, gudang_id)
                    )
                )
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=15, color="transparent"),
            ft.Row(
                [TemplateButton(
                    text="Enter",
                    style="outline",
                    width=200,
                    on_click=lambda e, gudang_id=Gudang._id: (
                        page.clean(),
                        barangPage(page, gudang_id)
                    )
                )],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
    )
    for Gudang in ListGudang
]

    grid_view = ft.GridView(
        expand=True,
        max_extent=300,
        spacing=10,
        run_spacing=10,
        padding=20,
        controls=gudang_cards
    )

    
    on_click_handler = [
        lambda e: print("Home clicked"),
        lambda e: print("Settings clicked"),
        lambda e: print("History clicked"),
        lambda e: createGudangOverlay(page)
    ]
    nav_items = [
        {
            "icon": ft.icons.HOME_OUTLINED,
            "selected_icon": ft.icons.HOME,
            "label": "Home",
        },
        {
            "icon": ft.icons.SETTINGS_OUTLINED,
            "selected_icon": ft.icons.SETTINGS,
            "label": "Settings",
        },
        {
            "icon": ft.icons.HISTORY_OUTLINED,
            "selected_icon": ft.icons.HISTORY,
            "label": "History",
        },
        {
            "icon": ft.icons.ADD_OUTLINED,
            "selected_icon": ft.icons.ADD,
            "label": "Create Gudang",
        },
    ]
    
    # Create layout
    page.appbar = TemplateAppBar(
        title="Storage Allocation Manager",
        actions=[
            ft.IconButton(ft.icons.LIGHT_MODE),
            ft.IconButton(ft.icons.SETTINGS),
        ]
    )
    
    page.navigation_rail = TemplateNavigationRail(
        destinations=nav_items,
        on_click_handlers=on_click_handler
    )
    
    page.add(
        ft.Row([
            page.navigation_rail,
            ft.VerticalDivider(width=1),
            grid_view
        ], expand=True)
    )

    # TemplateButton(
    #     text="Create",
    #     style="primary",
    #     on_click=lambda e, : (
    #         createGudangOverlay(page)
    #     )
    # ),    

# if __name__ == "__main__":
#     ft.app(gudangPage)