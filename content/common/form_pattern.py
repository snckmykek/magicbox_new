from kivy.lang.builder import Builder
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty, DictProperty
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard

Builder.load_file(r"content/common/form_pattern.kv")


class FormPattern(ModalView, MDCard, RoundedRectangularElevationBehavior):

    owner: ObjectProperty()  # Владелец формы, кто открыл
    parameters: DictProperty({})  # Передаются владельцу после закрытия формы

    def __init__(self, **kwargs):
        super(FormPattern, self).__init__(**kwargs)
        self.parameters = {}

    def on_dismiss(self):
        if self.owner:
            self.owner.after_dismiss_child(self.parameters)

    def after_dismiss_child(self, parameters):
        pass
