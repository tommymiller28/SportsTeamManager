# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Core views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),

    # Teams
    path('create_team/', views.create_team, name='create_team'),
    path('team/<int:team_id>/roster/', views.view_roster, name='view_roster'),
    path('team/<int:team_id>/add_player/', views.add_player, name='add_player'),
    path('team/<int:team_id>/join/', views.join_team, name='join_team'),

    # Stats
    path('add_stat/', views.add_stat, name='add_stat'),
    path('my_stats/', views.my_stats, name='my_stats'),
    path('view_stats/', views.view_stats, name='view_stats'),
    path('stats/hitting/', views.view_hitting_stats, name='view_hitting_stats'),
    path('pitching_stats/', views.view_pitching_stats, name='view_pitching_stats'),
    path('stats/', views.combined_stats, name='stats_combined'),
    path('player-stats/<int:player_id>/', views.player_game_log, name='player_game_log'),
    path('player-pitching-stats/<int:player_id>/',views.player_pitching_log, name='player_pitching_game_log'),

    # Schedule
    path('schedule/', views.schedule_view, name='schedule'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('create_game/', views.create_game, name='create_game'),
    path('game/<int:game_id>/edit/', views.edit_game_view, name='edit_game'),
    path('game/<int:game_id>/delete/', views.delete_game_view, name='delete_game'),

    # Hitting stats edit/delete
    path('player-stat/<int:stat_id>/edit/', views.edit_player_stat, name='edit_player_stat'),
    path('player-stat/<int:stat_id>/delete/', views.delete_player_stat, name='delete_player_stat'),

    # Pitching stats edit/delete
    path('pitching-stat/<int:stat_id>/edit/', views.edit_pitching_stat, name='edit_pitching_stat'),
    path('pitching-stat/<int:stat_id>/delete/', views.delete_pitching_stat, name='delete_pitching_stat'),
]
