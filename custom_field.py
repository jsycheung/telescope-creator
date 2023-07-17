'''
Define a custom wtforms field to set SelectMultipleField to checkboxes instead of a list of options.
'''
from wtforms import widgets, SelectMultipleField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def pre_validate(self, form):
        """pre_validation is disabled"""
