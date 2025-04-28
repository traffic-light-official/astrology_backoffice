from django import forms


class UserInfo(forms.Form):
    user_name = forms.CharField(label='Name', max_length=100, required=False)
    birth_date = forms.DateField(label='Birth date', required=False, widget=forms.DateInput({'type': 'date'}))
    birth_time = forms.TimeField(label='Birth time', required=False, widget=forms.TimeInput({'type': 'time'}))
    place_of_birth = forms.CharField(label='Place of birth', max_length=100, required=False)
    zodiac_sign = forms.CharField(label='Zodiac sign', max_length=100, required=False)
    chinese_zodiac_sign = forms.CharField(label='Chinese_zodiac', max_length=100, required=False)
    gender = forms.CharField(label='Gender', max_length=100, required=False)
    language = forms.CharField(label='Language', max_length=100, required=False)


class UserDialogs(forms.Form):
    def __init__(self, *args, readonly=False, **kwargs):
        super().__init__(*args, **kwargs)

        if readonly:
            for field in self.fields.values():
                field.widget.attrs['readonly'] = 'readonly'
                field.widget.attrs['disabled'] = 'disabled'


    role = forms.CharField(label='Role', max_length=50, widget=forms.TextInput())
    content = forms.CharField(label='Content', widget=forms.Textarea())


class Prompts(forms.Form):
    def __init__(self, *args, readonly=False, **kwargs):
        super().__init__(*args, **kwargs)

        if readonly:
            for field in self.fields.values():
                field.widget.attrs['readonly'] = 'readonly'
                field.widget.attrs['disabled'] = 'disabled'


    system_prompt = forms.CharField(label='SystemPrompt', widget=forms.Textarea())
    soft_prompt = forms.CharField(label='SoftPrompt', widget=forms.Textarea())
