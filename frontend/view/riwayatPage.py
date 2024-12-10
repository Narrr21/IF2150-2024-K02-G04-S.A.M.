import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialog,
    TemplateCard, TemplateListItem, TemplatePage,
    TemplateAppBar, TemplateNavigationRail
)
from backend.controller.riwayatManager import (
    RiwayatManager
)

dataRiwayat = RiwayatManager.get_all_riwayat()

print(dataRiwayat)


def riwayatPage(page: ft.Page):
    # Initialize page with template
    page.__class__ = TemplatePage
    page.title = "Page Riwayat"

    # Create sample content
    content = ft.Column([
        ft.Text("Riwayat", size=20, weight="bold"),
        ft.Column([
            TemplateListItem(
                title=RiwayatManager.translate_riwayat(riwayat._id),
                leading=ft.Icon(ft.icons.HISTORY),
                subtitle=riwayat.timestamp,
            ) for riwayat in dataRiwayat
        ]),
    ], scroll=ft.ScrollMode.AUTO)

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
    ft.app(riwayatPage)