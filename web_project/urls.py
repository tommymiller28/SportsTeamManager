from django.contrib import admin
from django.urls import path
from users import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", user_views.home, name="home"),
    path("dashboard/", user_views.dashboard, name="dashboard"),
    path("signup/", user_views.signup_view, name="signup"),
    path("login/", user_views.login_view, name="login"),
    path("logout/", user_views.logout_view, name="logout"),
    path("create_team/", user_views.create_team, name="create_team"),
]
