# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Team, Player, PlayerStat, Game, Sport, PitchingStat


# -------------------------------
# User Signup Form
# -------------------------------
class SignUpForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        help_text="Enter your full name."
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'role', 'password1', 'password2']


# -------------------------------
# Team Creation Form
# -------------------------------
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'coach', 'sport']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['coach'].queryset = CustomUser.objects.filter(role='coach')


# -------------------------------
# Add Player Form
# -------------------------------
class AddPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['full_name', 'position']


# -------------------------------
# Player Form (For Player Join)
# -------------------------------
class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['full_name', 'team', 'position']


# -------------------------------
# Player Stats Entry Form
# -------------------------------
class PlayerStatForm(forms.ModelForm):
    class Meta:
        model = PlayerStat
        fields = [
            'player',
            'team',
            'sport',
            'game_date',
            'at_bats',
            'hits',
            'runs',
            'rbis',
            'home_runs',
            'doubles',
            'triples',
            'stolen_bases',
            'walks',
            'hit_by_pitch',
            'strikeouts',
        ]

    def __init__(self, *args, **kwargs):
        coach = kwargs.pop('coach', None)
        super().__init__(*args, **kwargs)
        
        if coach:
            self.fields['team'].queryset = Team.objects.filter(coach=coach)
            self.fields['player'].queryset = Player.objects.filter(team__coach=coach)
            self.fields['sport'].queryset = Sport.objects.filter(
                id__in=Team.objects.filter(coach=coach).values_list('sport', flat=True)
            )
            

# -------------------------------
# Pitching Stats Entry Form
# -------------------------------
class PitchingStatForm(forms.ModelForm):
    class Meta:
        model = PitchingStat
        fields = [
            'player',
            'team',
            'sport',
            'game_date',
            'innings_pitched',
            'hits_allowed',
            'runs_allowed',
            'earned_runs',
            'walks',
            'strikeouts',
            'home_runs_allowed',
            'pitches_thrown',
        ]

    def __init__(self, *args, **kwargs):
        coach = kwargs.pop('coach', None)
        super().__init__(*args, **kwargs)
        if coach:
            self.fields['team'].queryset = Team.objects.filter(coach=coach)
            self.fields['player'].queryset = Player.objects.filter(team__coach=coach)
            self.fields['sport'].queryset = Sport.objects.filter(name="Baseball")


# -------------------------------
# Game Creation Form
# -------------------------------

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['team', 'opponent', 'date', 'location', 'team_score', 'opponent_score']

    def __init__(self, *args, **kwargs):
        coach = kwargs.pop('coach', None)
        super().__init__(*args, **kwargs)
        if coach:
            self.fields['team'].queryset = Team.objects.filter(coach=coach)


# -------------------------------
# Update Game Score Form
# -------------------------------
class UpdateScoreForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['team_score', 'opponent_score']
