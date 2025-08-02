from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True,null=True)
    full_name = models.CharField(
        _("full name"),
        max_length=255,
        blank=True, # Allow blank for flexibility, though you might make it required in forms
        help_text=_("your full name")
    )
    GENDER_CHOICES = [
        ('Female', _('Female')),
        ('Male', _('Male')),
        ('NA', _("I don't want to say")), # Or 'Unspecified', 'Prefer not to say'
    ]
    gender = models.CharField(
        _("gender"),
        max_length=20,
        choices=GENDER_CHOICES,
        default='NA', 
        blank=True,          
        help_text=_("your gender")
    )
    profile_picture = models.ImageField(
        _("profile picture"),
        upload_to='profile_pics/users/', 
        blank=True, 
        null=True, 
        help_text=_("The user's profile picture.")
    )
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the full_name.
        """
        return self.full_name or self.username




