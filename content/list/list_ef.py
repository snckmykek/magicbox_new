from kivy.lang.builder import Builder
from content.common.form_pattern import FormPattern


Builder.load_file(r"content/list/list_ef.kv")


class ListElementForm(FormPattern):

    def __init__(self, **kwargs):
        super(ListElementForm, self).__init__(**kwargs)

        self.parameters.update({'test': 1})