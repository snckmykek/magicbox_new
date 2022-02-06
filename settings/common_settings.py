from kivy.lang.builder import Builder
from content.common.form_pattern import FormPattern

Builder.load_file(r"settings/common_settings.kv")


class CommonSettingsForm(FormPattern):

    def __init__(self, **kwargs):
        super(CommonSettingsForm, self).__init__(**kwargs)
