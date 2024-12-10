import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialog,
    TemplateCard, TemplateListItem, TemplatePage,
    TemplateAppBar, TemplateNavigationRail
)
from const import DARK_TEXT
from backend.app import get_all_gudang


def gudangPage(page: ft.Page):
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
                            on_click=lambda e: print("View Details clicked")
                        ),
                        TemplateButton(
                            text="Edit",
                            style="secondary",
                            on_click=lambda e: print("Edit clicked")
                        ),
                        TemplateButton(
                            text="X",
                            style="outline",
                            on_click=lambda e: print("Delete clicked")
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
            "label": "Home"
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

if __name__ == "__main__":
    ft.app(gudangPage)