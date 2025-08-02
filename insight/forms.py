from django import forms
from .models import Channel

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'about', 'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Add topic name'}),
            'about': forms.TextInput(attrs={'placeholder': 'Add your description'}),
        }
