import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialog,
    TemplateCard, TemplateListItem, TemplatePage,
    TemplateAppBar, TemplateNavigationRail
)
from frontend.const import DARK_TEXT
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
        updated_max_capacity = (dlg.fields[1].value)
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
    dlg = TemplateDialog(
        title="Edit Gudang",
        content=[
            TemplateTextField(
                label="Name",
                hint_text="Enter new name",
                value=gudang.gudang_name
            ),
            TemplateTextField(
                label="Capacity",
                hint_text="Enter new capacity",
                value=gudang.capacity
            ),
            TemplateTextField(
                label="Max Capacity",
                hint_text="Enter new max capacity",
                value=gudang.max_capacity
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

def gudangPage(page: ft.Page) -> int:
    # Initialize page with template
    page.__class__ = TemplatePage
    page.title = "Storage Allocation Manager"

    ListGudang = get_all_gudang()
    gudang_cards = [
        TemplateCard(
            title=Gudang.gudang_name,
            content=ft.Column( 
            [
                ft.Text(
                        f"CAPACITY: {Gudang.capacity}/{Gudang.max_capacity}", 
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "FULL!" if Gudang.capacity == Gudang.max_capacity else "Available",
                        color="red" if Gudang.capacity == Gudang.max_capacity else "green",
                        text_align=ft.TextAlign.CENTER
                    ),
                
                ft.Divider(height=20, color="transparent"), 
                    
                ft.Row(
                     [
                        TemplateButton(
                            text="Enter",
                            style="primary",
                            on_click=lambda e, gudang_id=Gudang._id: (
                                page.clean(),
                                barangPage(page, gudang_id)
                            )
                        ),
                        TemplateButton(
                            text="Edit",
                            style="secondary",
                            on_click=lambda e, gudang_id=Gudang._id: (
                                editGudangOverlay(page, gudang_id)
                            )
                        ),
                        TemplateButton(
                            text="X",
                            style="outline",
                            on_click=lambda e, gudang_id=Gudang._id: (
                                deleteGudangOverlay(page, gudang_id)
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    width=float('inf')
                )
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float('inf')
        )
        )
        for Gudang in ListGudang
    ]

    grid_view = ft.GridView(
        expand=True,
        max_extent=250,
        spacing=10,
        run_spacing=10,
        padding=20,
        controls=gudang_cards
    )

    # Setup navigation rail
    nav_items = [
        {
            "icon": ft.icons.HOME_OUTLINED,
            "selected_icon": ft.icons.HOME,
            "label": "Home",
            "on_click": lambda e: print("Home clicked")
        },
        {
            "icon": ft.icons.SETTINGS_OUTLINED,
            "selected_icon": ft.icons.SETTINGS,
            "label": "Settings"
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
        destinations=nav_items
    )
    
    page.add(
        ft.Row([
            page.navigation_rail,
            ft.VerticalDivider(width=1),
            grid_view
        ], expand=True)
    )

# if __name__ == "__main__":
#     ft.app(gudangPage)