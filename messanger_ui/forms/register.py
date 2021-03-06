from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from client import create_new_user


class RegisterForm(GridLayout):
    def __init__(self, **kwargs):
        super(RegisterForm, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text="New Login:", font_size=40))
        self.login = TextInput(multiline=False, font_size=45, hint_text='Enter new login')
        self.add_widget(self.login)

        self.add_widget(Label(text='New Password', font_size=40))
        self.password = TextInput(multiline=False, font_size=45, hint_text='Your password', password=True)
        self.add_widget(self.password)

        self.submit = Button(text='Create account', font_size=40, background_color=(1, 0, 0, 0.8),
                             on_press=lambda *args: create_new_user(self.login.text, self.password.text, self))
        self.add_widget(self.submit)

        self.get_back_button = Button(text='Back to login', font_size=40,background_color=(0, 1, 0, 0.9))
        self.add_widget(self.get_back_button)

    def user_created_popup(self):
        layout = GridLayout(cols=1, padding=10)

        popup_label = Label(text=f"User {self.login.text} has been created! You can now log in")
        close_button = Button(text="Close")

        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title='User created',
                      content=layout,
                      size_hint=(None, None), size=(500, 500))
        popup.open()

        close_button.bind(on_press=popup.dismiss)
        self.login.text = ''
        self.password.text = ''

    def login_exists_popup(self):
        layout = GridLayout(cols=1, padding=10)

        popup_label = Label(text=f"{self.login.text } login is already in our database")
        close_button = Button(text="Try again")

        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title='Login exists',
                      content=layout,
                      size_hint=(None, None), size=(500, 500))
        popup.open()

        close_button.bind(on_press=popup.dismiss)
        self.login.text = ''
        self.password.text = ''

    def incorrect_login_popup(self):
        layout = GridLayout(cols=1, padding=10)

        popup_label = Label(text=f"Login {self.login.text} is incorrect\n"
                                 f"Please don't use special symbols and don't start login from number",halign="center")
        close_button = Button(text="Try")

        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title='Incorrect login',
                      content=layout,
                      size_hint=(None, None), size=(500, 500))
        popup.open()

        close_button.bind(on_press=popup.dismiss)
        self.login.text = ''
        self.password.text = ''
