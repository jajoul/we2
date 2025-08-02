# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from .models import User

class SignUpStep1Form(forms.Form):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'xxxx@email.com'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match.")
        
        return cleaned_data


class SignUpStep2Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profile_picture', 'full_name', 'gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'placeholder': 'Name'})

        self.fields['gender'].widget = forms.RadioSelect(choices=User.GENDER_CHOICES)
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            if profile_picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Profile picture cannot be larger than 5MB.")
        return profile_picture