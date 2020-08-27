from django import forms

class SettingsForm(forms.Form):

    base_url = forms.URLField()
    p_max = forms.CharField(max_length=50)
    p_min = forms.CharField(max_length=50)

