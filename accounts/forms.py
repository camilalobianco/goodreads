from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"

class ProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('bio','foto_de_perfil')
