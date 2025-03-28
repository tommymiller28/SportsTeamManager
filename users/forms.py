from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Team, Player  # Import your CustomUser model

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']  # Ensure 'role' is here

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})  # Add dropdown styling
    )


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
