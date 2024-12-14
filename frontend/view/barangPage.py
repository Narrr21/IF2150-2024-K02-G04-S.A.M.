import flet as ft
from frontend.template import (
    TemplateButton, TemplateTextField, TemplateDialog,
    TemplateCard, TemplateListItem, TemplatePage,
    TemplateAppBar, TemplateNavigationRail, TemplateDialogTextField
)
from backend.app import *

def deleteBarangOverlay(page: ft.Page, id: int, gudang_id: int, barang_page):
    def close_dlg(e):
        dlg.open = False
        page.update()

    def confirm_delete(e):
        update_barang_qty(id, gudang_id, 0)
        dlg.open = False
        # page.clean()
        barang_page.refresh_data()
        page.update()

    dlg = TemplateDialog(
        title="Confirm Delete",
        content="Are you sure you want to delete this barang?",
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

def updateBarangOverlay(page: ft.Page, id: int, gudang_id: int, barang_page):
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

    def validate_input(e, field, field_name):
        """ Validate input when the user types. """
        if field.value:
            try:
                if field_name == "quantity":
                    int(field.value)
                elif field_name == "size":
                    int(field.value)
                
                field.error_text = ""
                field.border_color = "gray"  
            except ValueError:
                field.error_text = f"{field_name.capitalize()} must be an integer!"
                field.border_color = "red"
        else:
            field.error_text = ""
            field.border_color = "gray"
        page.update()

    def save_changes(e):
        # Implement save changes logic here
        updated_name = dlg.fields[0].value
        updated_qty = (dlg.fields[1].value)
        updated_size = (dlg.fields[2].value)
        is_valid = True
        if updated_qty:
            try:
                updated_qty = int(updated_qty)
            except ValueError:
                dlg.fields[1].error_text = "Quantity must be an integer!"
                dlg.fields[1].border_color = "red"
                is_valid = False

        if updated_size:
            try:
                updated_size = int(updated_size)
            except ValueError:
                dlg.fields[1].error_text = "Size must be an integer!"
                dlg.fields[1].border_color = "red"
                is_valid = False

        listgud = get_all_gudang()
        for gudang in listgud:
            item_qty = 0
            for barang in gudang.list_barang:
                if get_barang(barang[0]).name == updated_name:
                    dlg.fields[0].error_text = "Name already exists!"
                    dlg.fields[0].border_color = "red"
                    is_valid = False
                    break
                if get_barang(barang[0])._id == id:
                    item_qty = barang[1]
            if gudang.capacity + item_qty*updated_size > gudang.max_capacity:
                dlg.fields[2].error_text = "Size too large! Gudang capacity exceeded!"
                dlg.fields[2].border_color = "red"
                is_valid = False
            

        if not is_valid:
            page.update()
            return
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
        barang_page.refresh_data()
        dlg.open = False
        page.update()
        

        

        # barangPage(page, gudang_id)
        

    
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
                value=str(num),
                on_change=lambda e: validate_input(e, dlg.fields[1], "quantity")
            ),
            TemplateTextField(
                label="Size",
                hint_text="Enter the new size of the barang (if changed)",
                width=300,
                value=str(barang.capacity),
                on_change=lambda e: validate_input(e, dlg.fields[2], "size")

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
        ],
    )
    dlg.content = ft.Column(dlg.fields, height=180)
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def addBarangOverlay(page: ft.Page, gudang_id: int, barang_page):
    listbar = get_all_barang()
    current_listbar = get_barang_by_gudang(get_gudang(gudang_id))
    for barang in current_listbar:
        for i in range(len(listbar)):
            if listbar[i]._id == barang._id:
                listbar.pop(i)
                break
    gudang = get_gudang(gudang_id)

    def close_dlg(e):
        dlg.open = False
        barang_page.refresh_data()
        page.update()

    def add_barangs(e, barang):
        if gudang.capacity + barang.capacity > gudang.max_capacity:
            dlg.fields[0].error_text = "Size too large! Gudang capacity exceeded!"
            dlg.fields[0].border_color = "red"
            page.update()
            return
        add_barang(barang, gudang, 1)
        close_dlg(e)


    dlg = TemplateDialogTextField(
        title="Add Barang",
        fields=[
            TemplateButton(
                text=Barang.name,
                style="primary",
                on_click=lambda e, barang=Barang: add_barangs(e, barang), 
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

def createBarangOverlay(page: ft.Page, id: int, barang_page):
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
            barang = Barang(name, size, "SKIBIDI", [])
            listbar = get_all_barang()
            for bar in listbar:
                if bar.name == name:
                    dlg.fields[0].error_text = "Name already exists!"
                    dlg.fields[0].border_color = "red"
                    page.update()
                    return
            gudang = get_gudang(id)
            if gudang.capacity + qty*size > gudang.max_capacity:
                dlg.fields[1].error_text = "Size and capacity exceeded!"
                dlg.fields[1].border_color = "red"
                dlg.fields[2].error_text = "Size and capacity exceeded!"
                dlg.fields[2].border_color = "red"
                page.update()
                return
            create_barang(barang, gudang, qty)
        dlg.open = False

        barang_page.refresh_data()
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

    dlg.content = ft.Column(dlg.fields, height=180)
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

class barangPage(ft.UserControl):
    #Initialize page with template
    def __init__(self,page: ft.Page, id: int):
        super().__init__()
        self.page = page
        self.id = id
        self.tempgudang = get_gudang(id)
        self.list_barang = get_barang_by_gudang(self.tempgudang)
        self.list_int_barang = [barang[1] for barang in self.tempgudang.list_barang]
        self.list_barang_and_int = [
            [self.list_barang[i],self.list_int_barang[i]] for i in range(len(self.list_barang))
        ]
        self.list_barang_and_int.sort(key=lambda x: x[1], reverse=False)
        self.filtered_list = self.list_barang_and_int

    def refresh_data(self):
        self.tempgudang = get_gudang(self.id)
        self.list_barang = get_barang_by_gudang(self.tempgudang)
        self.list_int_barang = [barang[1] for barang in self.tempgudang.list_barang]
        self.list_barang_and_int = [
            [self.list_barang[i],self.list_int_barang[i]] for i in range(len(self.list_barang))
        ]
        self.list_barang_and_int.sort(key=lambda x: x[1], reverse=False)
        self.filtered_list = self.list_barang_and_int

        self.refresh_content()


    def on_search_click(self,e):
        search_query =self.search_bar.value.lower()
        self.filtered_list = [
            item for item in self.list_barang_and_int
            if search_query in item[0].name.lower()
        ]
        self.refresh_content()

    def on_clear_search_click(self,e):
        self.search_bar.value = ""  # Clear the search bar
        self.filtered_list = self.list_barang_and_int  # Reset to show all the goods
        self.refresh_content()

    def refresh_content(self):
        self.content.controls.clear()
        self.content.controls.append(
            ft.Column(
                [
                    # Show "No result" message if no results found
                    ft.Text("No result", size=16, color="red") if len(self.filtered_list) == 0 else ft.Text(""),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    TemplateButton(
                                        "Edit",
                                        on_click=lambda e, barang=item[0]: updateBarangOverlay(self.page, barang._id, self.tempgudang._id,self)
                                    ),
                                    TemplateButton(
                                        "Delete",
                                        on_click=lambda e, barang=item[0]: deleteBarangOverlay(self.page, barang._id, self.tempgudang._id, self)
                                    ),
                                    TemplateListItem(
                                        title=item[0].name,
                                        subtitle=f"qty: {str(item[1])} \nsize: {str(item[0].capacity)}",
                                    )
                                ],
                                expand=True
                            )
                            for item in self.filtered_list
                        ],
                        expand=True
                    ),
                ],
                expand=True
            )
        )
        self.page.update()

    def build(self):
        self.search_bar = TemplateTextField(
            label="Search",
            hint_text="Search by name",
            # expand = True, 
            suffix = ft.IconButton(
                ft.icons.CLOSE,
                on_click=self.on_clear_search_click
            ), on_submit = self.on_search_click
        )

        self.content = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        self.refresh_content()

        return ft.Container(
        content=ft.Column(
            [
                # Search bar and Gudang name in the same column
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(self.search_bar, expand=True),
                                TemplateButton("Search", on_click=self.on_search_click),
                            ],
                            expand=True
                        ),
                        ft.Text(self.tempgudang.gudang_name, size=20, weight="bold"),
                        ft.Row(
                            [
                                TemplateButton("Create Barang", on_click=lambda e: createBarangOverlay(self.page, self.id, self)),
                                TemplateButton("Add Barang", on_click=lambda e: addBarangOverlay(self.page, self.id, self)),
                            ],
                        ),
                    ],
                    spacing=10,
                ),
                self.content
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            spacing=20 
        ),
        expand=True,
        padding=0,  # Remove padding
        alignment=ft.alignment.top_center  # Align container content to top-center
    )

# def barangPage(page: ft.Page, id: int):
#     # page.clean()
#     tempgudang = get_gudang(id)

#     list_barang = get_barang_by_gudang(tempgudang)
#     list_int_barang = []
#     for barang in tempgudang.list_barang:
#         list_int_barang.append(barang[1])

#     list_barang_and_int = []
#     for i in range(len(list_barang)):
#         list_barang_and_int.append([list_barang[i], list_int_barang[i]])

#     list_barang_and_int = sorted(list_barang_and_int, key=lambda x: x[1], reverse=False)
#     # Initialize page with template
#     page.__class__ = TemplatePage
#     page.title = "Page Barang"

#     # Create sample content


#     filtered_list = list_barang_and_int

#     def on_search_click(e):
#         nonlocal filtered_list
#         search_query =search_bar.value.lower()
#         filtered_list = [
#             item for item in list_barang_and_int
#             if search_query in item[0].name.lower()
#         ]
#         refresh_content()

#     def on_clear_search_click(e):
#         nonlocal filtered_list
#         search_bar.value = ""  # Clear the search bar
#         filtered_list = list_barang_and_int  # Reset to show all the goods
#         refresh_content()

#     search_bar = TemplateTextField(
#         label="Search",
#         hint_text="Search by name",
#         # expand = True, 
#         suffix = ft.IconButton(
#             ft.icons.CLOSE,
#             on_click=on_clear_search_click
#         ), on_submit = on_search_click
#     )


#     def refresh_content():
#         content.controls.clear()
#         content.controls.append(
#             ft.Column(
#                 [
#                     # Show "No result" message if no results found
#                     ft.Text("No result", size=16, color="red") if len(filtered_list) == 0 else ft.Text(""),
#                     ft.Column(
#                         [
#                             ft.Row(
#                                 [
#                                     TemplateButton(
#                                         "Edit",
#                                         on_click=lambda e, barang=item[0]: updateBarangOverlay(page, barang._id, tempgudang._id)
#                                     ),
#                                     TemplateButton(
#                                         "Delete",
#                                         on_click=lambda e, barang=item[0]: deleteBarangOverlay(page, barang._id, tempgudang._id)
#                                     ),
#                                     TemplateListItem(
#                                         title=item[0].name,
#                                         subtitle=f"qty: {str(item[1])} \nsize: {str(item[0].capacity)}",
#                                     )
#                                 ],
#                                 expand=True
#                             )
#                             for item in filtered_list
#                         ],
#                         expand=True
#                     ),
#                 ],
#                 expand=True
#             )
#         )
#         page.update()


#     content = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

#     refresh_content()

    
#     on_click_handler = [
#         lambda e: print("Home clicked"),
#         lambda e: print("Settings clicked"),
#         lambda e: print("History clicked"),
#         lambda e, gudang_id=id: createBarangOverlay(page, gudang_id),
#         lambda e, gudang_id=id: addBarangOverlay(page, gudang_id)
#     ]
#     # Setup navigation rail
#     nav_items = [
#         {
#             "icon": ft.icons.HOME_OUTLINED,
#             "selected_icon": ft.icons.HOME,
#             "label": "Home",
#         },
#         {
#             "icon": ft.icons.SETTINGS_OUTLINED,
#             "selected_icon": ft.icons.SETTINGS,
#             "label": "Settings",
#         },
#         {
#             "icon": ft.icons.HISTORY_OUTLINED,
#             "selected_icon": ft.icons.HISTORY,
#             "label": "History",
#         },
#         {
#             "icon": ft.icons.ADD_OUTLINED,
#             "selected_icon": ft.icons.ADD,
#             "label": "Create Barang",
#         },
#         {
#             "icon": ft.icons.ADD_OUTLINED,
#             "selected_icon": ft.icons.ADD,
#             "label": "Add Barang",
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
#         destinations=nav_items,
#         # on_click_handlers=on_click_handler
#     )
    
#     search_button =  TemplateButton("Search", on_click= on_search_click)
#     page.add(
#         ft.Row(
#             [ 
#                 page.navigation_rail,
#                 ft.Column(
#                     [
#                         ft.Row(
#                             [   
#                                 ft.Container(
#                                 content=search_bar,  # Wrap search_bar in a container
#                                 expand=True,  # This ensures it stretches
#                                 ),
#                                 ft.Container(
#                                     width = 10
#                                 ),
#                                 search_button,
#                             ],
#                             expand=False,
#                             alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                         ),
#                         ft.Text(tempgudang.gudang_name, size=20, weight="bold"),
#                         content,

#                     ],
#                     expand=True,
#                     alignment=ft.MainAxisAlignment.START,  # Align items in this column to the top

#                 )
#             ],
#             expand=True,
#             alignment=ft.CrossAxisAlignment.START  # Align NavigationRail and Column at the top

#         ),
#     )

# if __name__ == "__main__":
#     def main(page: ft.Page):
#         # Replace '1' with the appropriate gudang_id or fetch dynamically
#         barangPage(page, id=2)

#     ft.app(target=main)

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
