from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from forms.register import RegisterForm


class InterfaceManager(BoxLayout):

    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        self.register_form = RegisterForm()
        self.register_form.get_back_button.bind(on_press=self.show_second)

        self.second = Button(text="Second")
        self.second.bind(on_press=self.show_final)

        self.final = Label(text="Hello World")
        self.add_widget(self.register_form)

    def show_second(self, button):
        self.clear_widgets()
        self.add_widget(self.second)

    def show_final(self, button):
        self.clear_widgets()
        self.add_widget(self.final)


class MessangerApp(App):
    def build(self):
        return InterfaceManager()


MessangerApp().run()
