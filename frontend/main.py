import flet as ft
from template import (
    TemplateButton, TemplateTextField, TemplateDialog,
    TemplateCard, TemplateListItem, TemplatePage,
    TemplateAppBar, TemplateNavigationRail
)
from const import DARK_TEXT
from frontend.view.editGudang import showGudang

def main(page: ft.Page):
    # Initialize page with template
    page.__class__ = TemplatePage
    page.title = "Design System Showcase"


    # Create sample content
    content = ft.Column([
        ft.Text("Buttons", size=20, weight="bold"),
        ft.Row([
            TemplateButton("Primary Button", style="primary"),
            TemplateButton("Secondary Button", style="secondary"),
            TemplateButton("Outline Button", style="outline"),
        ]),
        
        ft.Divider(),
        ft.Text("Text Fields", size=20, weight="bold"),
        TemplateTextField(
            label="Sample Input",
            hint_text="Enter some text"
        ),
        
        ft.Divider(),
        ft.Text("Cards", size=20, weight="bold"),
        TemplateCard(
            title="Sample Card",
            content=ft.Text("This is a sample card with custom styling.")
        ),
        
        ft.Divider(),
        ft.Text("List Items", size=20, weight="bold"),
        ft.Column([
            TemplateListItem(
                title="List Item 1",
                subtitle="With subtitle",
                leading=ft.Icon(ft.icons.STAR),
                trailing=ft.Icon(ft.icons.ARROW_FORWARD_IOS)
            ),
            TemplateListItem(
                title="List Item 2",
                subtitle="Another item",
                leading=ft.Icon(ft.icons.FAVORITE),
            ),
        ]),
        
        ft.Divider(),
        ft.Text("Dialog", size=20, weight="bold"),
        TemplateButton(
            text="Show Dialog",
            on_click=showGudang
        ),
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
    ft.app(target=main) 