from django import forms


class DetectStampsImageForm(forms.Form):
    image = forms.ImageField()
