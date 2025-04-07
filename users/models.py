# users/models.py



from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone



# Custom User Model (Extends Django's AbstractUser)
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, default="Unknown User")  # Full name added

    ROLE_CHOICES = [
        ('coach', 'Coach'),
        ('player', 'Player'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')

    def __str__(self):
        return f"{self.full_name} - {self.role}"


# Sport Model
class Sport(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Team Model
class Team(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)  # NEW

    def __str__(self):
        return f"{self.name} ({self.sport.name})"
    

# Player Model
class Player(models.Model):
    full_name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True  # <== Important: allows optional
    )

    def __str__(self):
        return f"{self.full_name} ({self.position})"


# Player Stats

class PlayerStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    game_date = models.DateField()
    at_bats = models.PositiveIntegerField(default=0)
    hits = models.PositiveIntegerField(default=0)
    runs = models.PositiveIntegerField(default=0)
    rbis = models.PositiveIntegerField(default=0)
    home_runs = models.PositiveIntegerField(default=0)
    doubles = models.PositiveIntegerField(default=0)
    triples = models.PositiveIntegerField(default=0)
    stolen_bases = models.PositiveIntegerField(default=0)
    walks = models.PositiveIntegerField(default=0)
    hit_by_pitch = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.player.full_name} - {self.game_date} Stats"


# Pitching Stats
class PitchingStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    game_date = models.DateField(default=timezone.now)

    innings_pitched = models.DecimalField(max_digits=4, decimal_places=1)  # 4.1 innings etc.
    hits_allowed = models.PositiveIntegerField(default=0)
    runs_allowed = models.PositiveIntegerField(default=0)
    earned_runs = models.PositiveIntegerField(default=0)
    walks = models.PositiveIntegerField(default=0)
    strikeouts = models.PositiveIntegerField(default=0)
    home_runs_allowed = models.PositiveIntegerField(default=0)
    pitches_thrown = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.player.full_name} - {self.game_date} - {self.team.name}"

      
# Game Model
class Game(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    opponent = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    team_score = models.IntegerField(blank=True, null=True)
    opponent_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.team.name} vs {self.opponent} on {self.date.strftime('%Y-%m-%d')}"
