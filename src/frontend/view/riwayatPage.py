import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialog,
    TemplateCard, TemplateListItem, TemplatePage,
    TemplateAppBar, TemplateNavigationRail
)
from backend.controller.riwayatManager import (
    RiwayatManager
)



class riwayatPage(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.dataRiwayat = RiwayatManager.get_all_riwayat()
        self.dataRiwayat = sorted(self.dataRiwayat, key=lambda x: x.timestamp, reverse=True)

    def refreshScreen(self):
        self.content_area.clean()
        self.content_area.content = self.build()
        self.content_area.update()

    def build(self):
        return ft.Column([
            ft.Text("Riwayat", size=20, weight="bold"),
            ft.Column([
                TemplateListItem(
                    title=RiwayatManager.translate_riwayat(riwayat._id),
                    leading=ft.Icon(ft.icons.HISTORY),
                    subtitle=riwayat.timestamp,
                ) for riwayat in self.dataRiwayat
            ]),
        ], scroll=ft.ScrollMode.AUTO)

# dataRiwayat = RiwayatManager.get_all_riwayat()

# print(dataRiwayat)


# def riwayatPage(page: ft.Page):
#     # Initialize page with template
#     page.__class__ = TemplatePage
#     page.title = "Page Riwayat"

#     # Create sample content
#     content = ft.Column([
#         ft.Text("Riwayat", size=20, weight="bold"),
#         ft.Column([
#             TemplateListItem(
#                 title=RiwayatManager.translate_riwayat(riwayat._id),
#                 leading=ft.Icon(ft.icons.HISTORY),
#                 subtitle=riwayat.timestamp,
#             ) for riwayat in dataRiwayat
#         ]),
#     ], scroll=ft.ScrollMode.AUTO)

#     # Setup navigation rail
#     nav_items = [
#         {
#             "icon": ft.icons.HOME_OUTLINED,
#             "selected_icon": ft.icons.HOME,
#             "label": "Home"
#         },
#         {
#             "icon": ft.icons.SETTINGS_OUTLINED,
#             "selected_icon": ft.icons.SETTINGS,
#             "label": "Settings"
#         },
#         {
#             "icon": ft.icons.HISTORY_OUTLINED,
#             "selected_icon": ft.icons.HISTORY,
#             "label": "History"
#         },
#     ]
    
#     # Create layout
#     page.appbar = TemplateAppBar(
#         title="Design System",
#         actions=[
#             ft.IconButton(ft.icons.LIGHT_MODE),
#             ft.IconButton(ft.icons.SETTINGS),
#         ]
#     )
    
#     page.navigation_rail = TemplateNavigationRail(
#         destinations=nav_items
#     )
    
#     page.add(
#         ft.Row([
#             page.navigation_rail,
#             ft.VerticalDivider(width=1),
#             content,
#         ], expand=True)
#     )

# if __name__ == "__main__":
#     ft.app(riwayatPage)