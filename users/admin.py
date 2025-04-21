# users/admin.py

from django.contrib import admin
from .models import CustomUser, Team, Player, Sport, PlayerStat, PitchingStat, Game


# -----------------------------
# Custom User Admin
# -----------------------------
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')


# -----------------------------
# Team Admin
# -----------------------------
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'sport')
    search_fields = ('name',)
    list_filter = ('sport',)


# -----------------------------
# Player Admin
# -----------------------------
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team', 'position')
    exclude = ('user',)  # ✅ Remove user field from admin form
    list_filter = ('team',)
    search_fields = ('full_name', 'team__name')
    # ✅ Removed PlayerStatInline and PitchingStatInline to clean the form


# -----------------------------
# Sport Admin
# -----------------------------
@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name',)


# # -----------------------------
# Player Stat Admin
# -----------------------------
@admin.register(PlayerStat)
class PlayerStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'game_date', 'hits', 'runs', 'home_runs', 'rbis', 'strikeouts')
    list_filter = ('team', 'game_date')
    search_fields = ('player__full_name',)
    date_hierarchy = 'game_date'

    fields = (
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
    )


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
