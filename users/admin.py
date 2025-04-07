# users/admin.py

from django.contrib import admin
from .models import CustomUser, Sport, Team, Player, PlayerStat, PitchingStat, Game


# -----------------------------
# Custom User Admin
# -----------------------------
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'full_name', 'email')


# -----------------------------
# Sport Admin
# -----------------------------
@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# -----------------------------
# Team Admin
# -----------------------------
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'sport')
    list_filter = ('sport',)
    search_fields = ('name', 'coach__full_name')
    autocomplete_fields = ['coach']


# -----------------------------
# Player Stat Inline (Optional)
# -----------------------------
class PlayerStatInline(admin.TabularInline):
    model = PlayerStat
    extra = 1


class PitchingStatInline(admin.TabularInline):
    model = PitchingStat
    extra = 1


# -----------------------------
# Player Admin
# -----------------------------
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team', 'position', 'user')
    list_filter = ('team',)
    search_fields = ('full_name', 'team__name')
    inlines = [PlayerStatInline, PitchingStatInline]


# -----------------------------
# Player Stat Admin
# -----------------------------
@admin.register(PlayerStat)
class PlayerStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'game_date', 'hits', 'runs', 'home_runs', 'rbis')
    list_filter = ('team', 'game_date')
    search_fields = ('player__full_name',)
    date_hierarchy = 'game_date'


# -----------------------------
# Pitching Stat Admin
# -----------------------------
@admin.register(PitchingStat)
class PitchingStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'game_date', 'innings_pitched', 'strikeouts', 'earned_runs', 'hits_allowed')
    list_filter = ('team', 'game_date')
    search_fields = ('player__full_name',)
    date_hierarchy = 'game_date'


# -----------------------------
# Game Admin
# -----------------------------
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('team', 'opponent', 'date', 'location', 'team_score', 'opponent_score')
    list_filter = ('team', 'date')
    search_fields = ('opponent', 'location')
    date_hierarchy = 'date'
