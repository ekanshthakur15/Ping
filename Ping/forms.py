from django import forms
from .models import Pings

class PingForm(forms.ModelForm):
    body = forms.CharField(
        required= True,
        widget = forms.widgets.Textarea(
            attrs={
            "placeholder": "Write something...",
            "class": "textarea is-info is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = Pings
        exclude = {"user", }