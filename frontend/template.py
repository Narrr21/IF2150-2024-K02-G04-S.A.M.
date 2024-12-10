import flet as ft
from frontend.const import *

class TemplateButton(ft.ElevatedButton):
    def __init__(
        self,
        text: str,
        on_click=None,
        style="primary",
        **kwargs
    ):
        styles = {
            "primary": {
                "bgcolor": TURQUOISE,
                "color": DARK_TEXT,
                "style": ft.ButtonStyle(
                    color=DARK_TEXT,
                    bgcolor=ft.colors.with_opacity(0.8, TURQUOISE),
                ),
            },
            "secondary": {
                "bgcolor": CAMBRIDGE_BLUE,
                "color": "white",
                "style": ft.ButtonStyle(
                    color="white",
                    bgcolor=ft.colors.with_opacity(0.8, CAMBRIDGE_BLUE),
                ),
            },
            "outline": {
                "bgcolor": "transparent",
                "color": TURQUOISE,
                "style": ft.ButtonStyle(
                    color=TURQUOISE,
                    bgcolor={"hovered": TURQUOISE, "": "transparent"},
                    overlay_color={"hovered": ft.colors.with_opacity(0.1, TURQUOISE)},
                    side=ft.BorderSide(2, TURQUOISE),
                ),
            }
        }
        
        style_props = styles.get(style, styles["primary"])
        super().__init__(
            text=text,
            on_click=on_click,
            **style_props,
            **kwargs
        )

class TemplateTextField(ft.TextField):
    def __init__(
        self,
        label: str,
        hint_text: str = None,
        **kwargs
    ):
        super().__init__(
            label=label,
            hint_text=hint_text,
            border_color=CAMBRIDGE_BLUE,
            focused_border_color=TURQUOISE,
            cursor_color=TURQUOISE,
            **kwargs
        )

class TemplateDialog(ft.AlertDialog):
    def __init__(
        self,
        title: str,
        content: str,
        actions=None,
        **kwargs
    ):
        if actions is None:
            actions = [
                TemplateButton("OK", style="primary"),
                TemplateButton("Cancel", style="outline")
            ]
            
        super().__init__(
            title=ft.Text(title, size=16, weight="bold"),
            content=ft.Text(content),
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
            **kwargs
        )

class TemplateCard(ft.Card):
    def __init__(
        self,
        title: str = None,
        content: any = None,
        **kwargs
    ):
        super().__init__(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(title, size=16, weight="bold") if title else None,
                    content if content else None,
                ], tight=True),
                padding=20,
            ),
            elevation=1,
            **kwargs
        )

class TemplateListItem(ft.ListTile):
    def __init__(
        self,
        title: str,
        subtitle: str = None,
        leading=None,
        trailing=None,
        **kwargs
    ):
        super().__init__(
            title=ft.Text(title),
            subtitle=ft.Text(subtitle) if subtitle else None,
            leading=leading,
            trailing=trailing,
            **kwargs
        )

class TemplatePage(ft.Page):
    def __init__(self, **kwargs):
        super().__init__(
            theme=ft.Theme(
                color_scheme=ft.ColorScheme(
                    primary=TURQUOISE,
                    secondary=CAMBRIDGE_BLUE,
                ),
            ),
            **kwargs
        )
        self.padding = 20
        self.spacing = 20
        self.bgcolor = "#FFFFFF"

class TemplateAppBar(ft.AppBar):
    def __init__(
        self,
        title: str,
        actions=None,
        **kwargs
    ):
        super().__init__(
            title=ft.Text(title, size=20, weight="bold", color=DARK_TEXT),
            bgcolor=TURQUOISE,
            actions=actions,
            **kwargs
        )

class TemplateNavigationRail(ft.NavigationRail):
    def __init__(
        self,
        destinations: list,
        selected_index=0,
        on_change=None,
        **kwargs
    ):
        destinations_ = [
            ft.NavigationRailDestination(
                icon=ft.Icon(destination["icon"], size=24, color=DARK_TEXT),
                selected_icon=ft.Icon(destination["selected_icon"], size=24),
                label_content=ft.Text(destination["label"], size=14, weight="bold", color=DARK_TEXT),
            ) for destination in destinations
        ]
        super().__init__(
            destinations=destinations_,
            selected_index=selected_index,
            on_change=on_change,
            bgcolor=CAMBRIDGE_BLUE,
            extended=True,
            **kwargs
        )
