from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Team, Player  # Import your CustomUser model

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, help_text="Enter your full name.")

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'role', 'password1', 'password2']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'coach']
        

class AddPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['full_name', 'position', 'user']


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['full_name', 'team', 'position']
