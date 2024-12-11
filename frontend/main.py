import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialog,
    TemplateCard, TemplateListItem, TemplatePage,
    TemplateAppBar, TemplateNavigationRail
)
from frontend.view.loginPage import LoginPage
from frontend.view.barangPage import barangPage
from frontend.view.gudangPage import *



def main(page: ft.Page):
    # Initialize page with template
    page.__class__ = TemplatePage
    page.title = "Storage Allocation Manager"

    def show_gudang_page():
        page.clean()
        gudangPage(page)
        page.update()

    def show_barang_page(id: int):
        page.clean()
        barangPage(page, id)
        page.update()
    
    def handle_login(username, password, isLoggedIn, message):
        # TODO: Implement actual login logic
        print(f"Login attempt - Username: {username}, Password: {password}")
        # For now, just switch to main content
        if (isLoggedIn):
            page.clean()
            show_main_content()
            page.update()
        else:
            show_gudang_page() # DEBUGGING
            show_error(message)
            
    def show_error(message: str):
        dialog = TemplateDialog(
            title="Error",
            content=message
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def show_main_content():
        # Your existing main content setup
        content_area = ft.Container(
            content=ft.Column([
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
                on_click=show_dialog
            ),
        ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )
        
        def route_change(route):
            # selected_index = page.navigation_rail.selected_index
            selected_index = route.control.selected_index
            content_area.clean()
            
            if selected_index == 0:
                content_area.content = gudangPage()
            elif selected_index == 1:
                content_area.content = gudangPage()
            elif selected_index == 2:
                content_area.content = gudangPage()
            elif selected_index == 3:
                content_area.content = gudangPage()
                
            page.update()
            
        def show_dialog(e):
            dialog = TemplateDialog(
                title="Sample Dialog",
                content="This is a sample dialog with custom styling."
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
            
        # Setup navigation rail
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
            title="Design System",
            actions=[
                ft.IconButton(ft.icons.LIGHT_MODE),
                ft.IconButton(ft.icons.SETTINGS),
            ]
        )
        
        page.navigation_rail = TemplateNavigationRail(
            destinations=nav_items,
            on_change=route_change
        )
        
        page.add(
            ft.Row([
                page.navigation_rail,
                ft.VerticalDivider(width=1),
                content_area,
            ], expand=True)
        )

    # Start with login page
    login_page = LoginPage(on_login=handle_login)
    # barang_page = barangPage(page, 1)
    page.add(login_page)
    # page.add(barang_page)

if __name__ == "__main__":
    ft.app(target=main) 