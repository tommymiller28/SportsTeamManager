from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, default="Unknown User")  # Add default value

    ROLE_CHOICES = [
        ('coach', 'Coach'),
        ('player', 'Player'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')

    def __str__(self):
        return f"{self.full_name} - {self.role}"


### Define Models for Teams & Players
    
from django.contrib.auth.models import User
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Player(models.Model):
    full_name = models.CharField(max_length=100)  # Changed from 'name'
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
                return f"{self.full_name} ({self.position})"
