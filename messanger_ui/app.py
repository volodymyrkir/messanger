from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.chat import ChatPage


class InterfaceManager(BoxLayout):

    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        self.login_form = LoginForm(self)
        self.login_form.register_button.bind(on_press=self.show_register)

        self.register_form = RegisterForm()
        self.register_form.get_back_button.bind(on_press=self.show_login)

        self.add_widget(self.login_form)

    def show_register(self, button=None):
        self.clear_widgets()
        self.add_widget(self.register_form)

    def show_login(self, button):
        self.clear_widgets()
        self.add_widget(self.login_form)

    def show_chat(self, login, client, another_user_id):
        self.clear_widgets()
        chat_page = ChatPage(login, client, another_user_id)
        self.add_widget(chat_page)


class MessangerApp(App):
    def build(self):
        return InterfaceManager()


MessangerApp().run()
