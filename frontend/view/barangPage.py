import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialog,
    TemplateCard, TemplateListItem, TemplatePage,
    TemplateAppBar, TemplateNavigationRail
)
from backend.app import (
    get_barang_by_gudang,
    get_gudang
)


tempgudang = get_gudang(1)

list_barang = get_barang_by_gudang(tempgudang)

print(list_barang)


def barangPage(page: ft.Page):
    # Initialize page with template
    page.__class__ = TemplatePage
    page.title = "Page Barang"

    # Create sample content
    content = ft.Column(
    [
        ft.Text(tempgudang.gudang_name, size=20, weight="bold"),
        ft.Column(
            [
                ft.Row(
                    [
                        TemplateButton("Edit"),
                        TemplateButton("Delete"),

                        TemplateListItem(
                            title=barang.name,
                            subtitle=barang.capacity,
                            leading=ft.Icon(ft.icons.HISTORY),
                        )
                    ]
                ) for barang in list_barang
            ]
        ),
    ],
    scroll=ft.ScrollMode.AUTO
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
        {
            "icon": ft.icons.HISTORY_OUTLINED,
            "selected_icon": ft.icons.HISTORY,
            "label": "History"
        },
    ]
    
    # Create layout
    page.appbar = TemplateAppBar(
        title="Design System",
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
            content,
        ], expand=True)
    )

if __name__ == "__main__":
    ft.app(barangPage)