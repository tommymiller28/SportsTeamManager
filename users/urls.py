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

    # Schedule
    path('schedule/', views.schedule_view, name='schedule'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('create_game/', views.create_game, name='create_game'),
]
