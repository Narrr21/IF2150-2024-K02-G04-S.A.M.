import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialog,
    TemplateCard, TemplateListItem, TemplatePage,
    TemplateAppBar, TemplateNavigationRail, TemplateDialogTextField
)
from backend.app import *

def deleteBarangOverlay(page: ft.Page, id: int, gudang_id: int):
    def close_dlg(e):
        dlg.open = False
        page.update()

    def confirm_delete(e):
        delete_barang(id)
        dlg.open = False
        page.clean()
        barangPage(page, gudang_id)
        page.update()

    dlg = TemplateDialog(
        title="Confirm Delete",
        content=ft.Text("Are you sure you want to delete this barang?"),
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

def updateBarangOverlay(page: ft.Page, id: int, gudang_id: int):
    barang = get_barang(id)
    num = 0
    listbar = get_barang_by_gudang(get_gudang(gudang_id))
    for i in range(len(listbar)):
        if listbar[i]._id == barang._id:
            num = listbar[i]._id
            break

    def close_dlg(e):
        dlg.open = False
        page.update()

    def save_changes(e):
        # Implement save changes logic here
        updated_name = dlg.fields[0].value
        updated_qty = (dlg.fields[1].value)
        updated_size = (dlg.fields[2].value)
        if updated_name:
            barang.name = updated_name
        if updated_qty:
            # list_barang = get_barang_by_gudang(get_gudang(gudang_id))
            # for i in range(len(list_barang)):
            #     if list_barang[i]._id == barang._id:
            #         list_barang[i] = (barang._id, int(updated_qty))
            #         break
            # gudang = get_gudang(gudang_id)
            # gudang.list_barang = list_barang
            # update_gudang(gudang)
            print(f"Updated qty: {updated_qty}")
            # try:
            updated_qty = int(updated_qty)
            # except ValueError:
            #     print("Invalid quantity value")
            update_barang_qty(barang._id, gudang_id, updated_qty)
        if updated_size:
            barang.capacity = int(updated_size)

        num = 0
        update_barang(barang)
        dlg.open = False
        page.clean()
        barangPage(page, gudang_id)

    
    dlg = TemplateDialogTextField(
        title="Edit Barang",
        fields=[
            TemplateTextField(
                label="Barang Name",
                hint_text="Enter the name of the barang (if changed)",
                width=300,
                autofocus=True,
                value=barang.name
            ),
            TemplateTextField(
                label="Quantity",
                hint_text="Enter the quantity of the barang (if changed)",
                width=300,
                value=str(num)
            ),
            TemplateTextField(
                label="Size",
                hint_text="Enter the new size of the barang (if changed)",
                width=300,
                value=str(barang.capacity)
            ),
        ],
        actions=[
            TemplateButton(
                text="Save Changes",
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
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def addBarangOverlay(page: ft.Page, gudang_id: int):
    listbar = get_barang_by_gudang(get_gudang(gudang_id))

    def close_dlg(e):
        dlg.open = False
        page.update()

    def add_barang(e, barang):
        # adding 1 barang
        update_barang_qty(barang_id=barang._id, gudang_id=gudang_id, qty=1)
        print(f"Added barang: {barang.name} to gudang {gudang_id}")

    dlg = TemplateDialogTextField(
        title="Add Barang",
        fields=[
            TemplateButton(
                text=Barang.name,
                style="primary",
                on_click=lambda e, barang=Barang: add_barang(e, barang)
            ) for Barang in listbar
        ],
        actions=[
            TemplateButton(
                text="Close",
                style="secondary",
                on_click=close_dlg
            ),
        ]
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def createBarangOverlay(page: ft.Page, id: int):
    def close_dlg(e):
        dlg.open = False
        page.update()

    def save_changes(e):
        # Implement save changes logic here
        name = dlg.fields[0].value
        qty = dlg.fields[1].value
        size = dlg.fields[2].value
        if name and qty and size:
            qty = int(qty)
            size = int(size)
            barang = Barang(name, size, "SKIBIDI")
            gudang = get_gudang(id)
            create_barang(barang, gudang, qty)
        dlg.open = False
        page.clean()
        barangPage(page, id)
        page.update()
        
    dlg = TemplateDialogTextField(
        title="Create Barang",
        fields=[
            TemplateTextField(
                label="Barang Name",
                hint_text="Enter the name of the barang",
                width=300,
                autofocus=True
            ),
            TemplateTextField(
                label="Quantity",
                hint_text="Enter the quantity of the barang",
                width=300
            ),
            TemplateTextField(
                label="Size",
                hint_text="Enter the size of the barang",
                width=300
            ),
        ],
        actions=[
            TemplateButton(
                text="Create Barang",
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

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def barangPage(page: ft.Page, id: int):
    # page.clean()
    tempgudang = get_gudang(id)

    list_barang = get_barang_by_gudang(tempgudang)
    list_int_barang = []
    for barang in tempgudang.list_barang:
        list_int_barang.append(barang[1])

    list_barang_and_int = []
    for i in range(len(list_barang)):
        list_barang_and_int.append([list_barang[i], list_int_barang[i]])

    list_barang_and_int = sorted(list_barang_and_int, key=lambda x: x[1], reverse=False)
    # Initialize page with template
    page.__class__ = TemplatePage
    page.title = "Page Barang"

    # Create sample content

    search_bar = TemplateTextField("Search")

    content = ft.Column(
    [
        ft.Row(
            [
                ft.Container(search_bar, expand=True), 
                TemplateButton("Enter")
            ],             
            expand=True
        ),
        ft.Text(tempgudang.gudang_name, size=20, weight="bold"),
        ft.Column(
            [
                ft.Row(
                    [
                        TemplateButton("Edit", on_click=lambda e: updateBarangOverlay(page, id, tempgudang._id)),
                        TemplateButton("Delete", on_click=lambda e: deleteBarangOverlay(page, id, tempgudang._id)),

                        TemplateListItem(
                            title=item[0].name,
                            subtitle=f"qty: {str(item[1])} \nsize: {str(item[0].capacity)}",
                            leading=ft.Icon(ft.icons.HISTORY),
                        )
                    ],
                    expand=True
                ) for item in list_barang_and_int
            ], 
        )
    ],
    scroll=ft.ScrollMode.AUTO,
    expand=True
)
    
    on_click_handler = [
        lambda e: print("Home clicked"),
        lambda e: print("Settings clicked"),
        lambda e: print("History clicked"),
        lambda e, gudang_id=id: createBarangOverlay(page, gudang_id),
        lambda e, gudang_id=id: addBarangOverlay(page, gudang_id)
    ]
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
            "label": "Create Barang",
        },
        {
            "icon": ft.icons.ADD_OUTLINED,
            "selected_icon": ft.icons.ADD,
            "label": "Add Barang",
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
        on_click_handlers=on_click_handler
    )
    

    page.add(
        ft.Row([
            page.navigation_rail,
            ft.VerticalDivider(width=1),
            content,

            ], 
        
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START 
            )
    )

# if __name__ == "__main__":
#     ft.app(barangPage)

# class BarangPage(ft.UserControl):
#     def __init__(self, id: int):
#         super().__init__()
#         self.id = id  # Store the ID of the gudang
#         self.tempgudang = get_gudang(id)  # Get gudang data
#         self.list_barang = get_barang_by_gudang(self.tempgudang)  # Fetch barang data
#         self.list_int_barang = [barang[1] for barang in self.tempgudang.list_barang]
#         # Combine barang names and quantities
#         self.list_barang_and_int = [
#             [self.list_barang[i], self.list_int_barang[i]]
#             for i in range(len(self.list_barang))
#         ]

#     def build(self):
#         # Main content
#         content = ft.Column(
#             [
#                 ft.Text(self.tempgudang.gudang_name, size=20, weight="bold"),
#                 ft.Column(
#                     [
#                         ft.Row(
#                             [
#                                 TemplateButton("Edit"),
#                                 TemplateButton("Delete"),
#                                 TemplateListItem(
#                                     title=item[0].name,
#                                     subtitle="qty: " + str(item[1]),
#                                     leading=ft.Icon(ft.icons.HISTORY),
#                                 ),
#                             ]
#                         )
#                         for item in self.list_barang_and_int
#                     ]
#                 ),
#             ],
#             scroll=ft.ScrollMode.AUTO,
#         )

#         # Navigation rail items
#         nav_items = [
#             {
#                 "icon": ft.icons.HOME_OUTLINED,
#                 "selected_icon": ft.icons.HOME,
#                 "label": "Home",
#             },
#             {
#                 "icon": ft.icons.SETTINGS_OUTLINED,
#                 "selected_icon": ft.icons.SETTINGS,
#                 "label": "Settings",
#             },
#             {
#                 "icon": ft.icons.HISTORY_OUTLINED,
#                 "selected_icon": ft.icons.HISTORY,
#                 "label": "History",
#             },
#         ]

#         # Layout structure
#         return ft.Row(
#             [
#                 TemplateNavigationRail(destinations=nav_items),
#                 ft.VerticalDivider(width=1),
#                 content,
#             ],
#             expand=True,
#         )