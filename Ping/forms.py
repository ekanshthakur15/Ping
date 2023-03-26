from django import forms
from .models import Pings

class PingForm(forms.ModelForm):
    body = forms.CharField(
        required= True,
        widget = forms.widgets.TextInput(
            attrs={
            "placeholder": "Write something...",
            "class": "textarea is-info is-small",
            }
        ),
        label="",
    )

    class Meta:
        model = Pings
        exclude = {"user", "parent", "likes"}