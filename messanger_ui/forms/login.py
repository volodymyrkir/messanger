from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window  # key press(enter) to login
from client import check_login_correctness


class LoginForm(GridLayout):
    def __init__(self, interface_manager):
        super(LoginForm, self).__init__()
        self.interface_manager = interface_manager
        self.cols = 2
        login_label = Label(text="Login:", font_size=40)
        self.add_widget(login_label)
        self.login = TextInput(multiline=False, font_size=45, hint_text='Enter login')
        self.add_widget(self.login)

        self.add_widget(Label(text='Password:', font_size=40))
        self.password = TextInput(multiline=False, font_size=45, hint_text='Enter password', password=True)
        self.add_widget(self.password)

        self.add_widget(Label(text='Companion', font_size=40))
        self.another_user = TextInput(multiline=False, font_size=45, hint_text='Companion login')
        self.add_widget(self.another_user)

        self.register_button = Button(text='Register', font_size=40, background_color=(1, 0, 0, 0.8))
        self.add_widget(self.register_button)

        self.login_button = Button(text='Log in', font_size=40, background_color=(0, 1, 0, 0.9),
                                   on_press=lambda *args: check_login_correctness(self.login.text, self.password.text,
                                                                                  self.another_user.text, self))
        self.add_widget(self.login_button)

    def incorrect_data_popup(self, another=False):
        layout = GridLayout(cols=1, padding=10)
        popup_text = "Wrong companion" if another else "Wrong login or password"
        popup_label = Label(text=popup_text, halign="center")
        close_button = Button(text="Try again")

        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title='User created',
                      content=layout,
                      size_hint=(None, None), size=(500, 500))
        popup.open()
        close_button.bind(on_press=popup.dismiss)
        self.login.text = ''
        self.password.text = ''

    def login_successful(self, login, client, another_user_id):
        self.interface_manager.show_chat(login, client, another_user_id)
