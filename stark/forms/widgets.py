from django import forms


class DateTimePickerInput(forms.TextInput):
    """
    自定义forms的TextInput渲染的html内容
    """
    template_name = 'stark/forms/widgets/datetime_picker.html'
