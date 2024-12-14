import flet as ft
from frontend.template import (
    TemplateDialog, TemplatePage,
    TemplateAppBar, TemplateNavigationRail
)
from frontend.view.loginPage import LoginPage
from frontend.view.riwayatPage import riwayatPage
from frontend.view.gudangPage import gudangPage, moveBarangOverlay, removeBarangOverlay



def main(page: ft.Page):
    # Initialize page with template
    page.__class__ = TemplatePage
    page.title = "Storage Allocation Manager"
    page.window.center()
    
    # def show_gudang_page():
    #     page.clean()
    #     gudangPage(page)
    #     page.update()

    # def show_barang_page(id: int):
    #     page.clean()
    #     barangPage(page, id)
    #     page.update()
    
    def handle_login(username, password, isLoggedIn, message):
        # TODO: Implement actual login logic
        print(f"Login attempt - Username: {username}, Password: {password}")
        # For now, just switch to main content
        isLoggedIn = True
        if (isLoggedIn):
            page.clean()
            show_main_content()
            page.update()
        else:
            show_error(message)
            
    def show_error(message: str):
        dialog = TemplateDialog(
            title="Error",
            content=message
        )
        page.show_dialog(dialog)
                
    def show_dialog(e):
        dialog = TemplateDialog(
            title="Sample Dialog",
            content="This is a sample dialog with custom styling."
        )
        page.show_dialog(dialog)

    # Pages
    login_page = LoginPage(page, handle_login)
    # riwayat_page = riwayatPage(page)
    
    def on_page_resize(e):
        login_page.height = page.window.height
        login_page.update()
    
    page.on_resized = on_page_resize

    def show_main_content():
        # Your existing main content setup
        content_area = ft.Container(expand=True)
        gudang_page = gudangPage(page, content_area)

        content_area.content = gudang_page
        
        def route_change(route):
            # selected_index = page.navigation_rail.selected_index
            selected_index = route.control.selected_index
            content_area.clean()
            
            if selected_index == 0:
                content_area.content = gudang_page
            elif selected_index == 1:
                moveBarangOverlay(page,gudang_page)
                page.update()
            elif selected_index == 2:
                removeBarangOverlay(page, gudang_page)
            elif selected_index == 3:
                content_area.content = riwayatPage(page)
                
            page.update()
            
        # Setup navigation rail
        nav_items = [
        {
            "icon": ft.icons.HOME_OUTLINED,
            "selected_icon": ft.icons.HOME,
            "label": "Home",
        },
        {
            "icon": ft.icons.DRIVE_FILE_MOVE_OUTLINED,
            "selected_icon": ft.icons.DRIVE_FILE_MOVE,
            "label": "Move Barang",
        },
        {
            "icon": ft.icons.DELETE_FOREVER_OUTLINED,
            "selected_icon": ft.icons.DELETE_FOREVER,
            "label": "Delete Barang from DB",
        },
        {
            "icon": ft.icons.HISTORY_OUTLINED,
            "selected_icon": ft.icons.HISTORY,
            "label": "History",
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
    # barang_page = barangPage(page, 1)
    page.add(login_page)
    # page.add(barang_page)

if __name__ == "__main__":
    ft.app(target=main) 