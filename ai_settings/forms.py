from django import forms


class Prompts(forms.Form):
    def __init__(self, *args, readonly=False, **kwargs):
        super().__init__(*args, **kwargs)

        if readonly:
            for field in self.fields.values():
                field.widget.attrs['readonly'] = 'readonly'
                field.widget.attrs['disabled'] = 'disabled'


    system_prompt = forms.CharField(label='SystemPrompt', widget=forms.Textarea())
    soft_prompt = forms.CharField(label='SoftPrompt', widget=forms.Textarea())
