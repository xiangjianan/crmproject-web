from django import forms


class BootStrapModelForm(forms.ModelForm):
    """
    ModelForm配置：统一为字段添加BootStrap样式
    """

    def __init__(self, *args, **kwargs):
        super(BootStrapModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
