import flet as ft
from frontend.template import TemplateCard, TemplateTextField, TemplateButton
from backend.login.loginManager import LoginManager


class LoginPage(ft.UserControl):
    login_manager = LoginManager()

    def __init__(self, page: ft.Page, on_login=None):
        super().__init__()
        self.on_login = on_login
        self.page = page

    def build(self):
        self.username_field = TemplateTextField(
            label="Username", hint_text="Enter your username", width=300, autofocus=True
        )

        self.password_field = TemplateTextField(
            label="Password",
            hint_text="Enter your password",
            password=True,
            can_reveal_password=True,
            width=300,
        )

        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Login", size=20, weight="bold"),
                        self.username_field,
                        self.password_field,
                        ft.Container(height=20),  # Spacing
                        TemplateButton(
                            text="Login",
                            style="primary",
                            width=300,
                            on_click=self.handle_login,
                        ),
                        ft.Container(height=10),  # Spacing
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                )
            ],
            expand=True,
            height=self.page.height,
        )

    def handle_login(self, e):
        if self.on_login:
            username = self.username_field.value
            password = self.password_field.value
            [isLoggedIn, message] = self.login_manager.login(
                username=username, password=password
            )
            self.on_login(
                username=username,
                password=password,
                isLoggedIn=isLoggedIn,
                message=message,
            )
