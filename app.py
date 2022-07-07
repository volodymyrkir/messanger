from functools import partial
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from client import create_new_user


class InterfaceManager(BoxLayout):

    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        self.first = RegisterForm()
        self.first.get_back_button.bind(on_press=self.show_second)

        self.second = Button(text="Second")
        self.second.bind(on_press=self.show_final)

        self.final = Label(text="Hello World")
        self.add_widget(self.first)

    def show_second(self, button):
        self.clear_widgets()
        self.add_widget(self.second)

    def show_final(self, button):
        self.clear_widgets()
        self.add_widget(self.final)


class RegisterForm(GridLayout):
    def __init__(self, **kwargs):
        super(RegisterForm, self).__init__(**kwargs)

        self.inside = GridLayout()
        self.cols = 2

        self.add_widget(Label(text="Login:", font_size=40))
        self.login = TextInput(multiline=False, font_size=60, hint_text='Enter login')
        self.add_widget(self.login)

        self.add_widget(Label(text='Password', font_size=40))
        self.password = TextInput(multiline=False, font_size=60, hint_text='Enter password', password=True)
        self.add_widget(self.password)

        self.submit = Button(text='Submit', font_size=40,
                             on_press=lambda *args: create_new_user(self.login.text, self.password.text, self))
        self.add_widget(self.submit)

        self.get_back_button = Button(text='Back to login', font_size=40)
        self.add_widget(self.get_back_button)

    def user_created(self):
        layout = GridLayout(cols=1, padding=10)

        popup_label = Label(text=f"User {self.login.text} has been created! You can now log in")
        close_button = Button(text="Back to main menu")

        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        # Instantiate the modal popup and display
        popup = Popup(title='User created',
                      content=layout,
                      size_hint=(None, None), size=(200, 200))
        popup.open()

        # Attach close button press with popup.dismiss action
        close_button.bind(on_press=popup.dismiss)
        self.login.text = ''
        self.password.text = ''


class MessangerApp(App):
    def build(self):
        return InterfaceManager()


MessangerApp().run()
