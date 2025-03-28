from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_team/', views.create_team, name='create_team'),
    path('team/<int:team_id>/roster/', views.view_roster, name='view_roster'),  # ✅ New route
    path('create_player/', views.create_player, name='create_player'),
    path('team/<int:team_id>/add_player/', views.add_player, name='add_player'),
    path('team/<int:team_id>/join/', views.join_team, name='join_team'),
    path('team/<int:team_id>/roster/', views.view_roster, name='view_roster'),
]
]
