from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', user_views.dashboard, name='dashboard'),
    path('signup/', user_views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Default Django login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
