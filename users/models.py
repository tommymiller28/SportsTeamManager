from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('coach', 'Coach'),
        ('player', 'Player'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')

    # Fix reverse accessor clashes by setting related_name attributes
    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_permissions', blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"
