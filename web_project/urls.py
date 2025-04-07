# web_project/urls.py ✅
from django.contrib import admin
from django.urls import path, include  # ✅ include is required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # ✅ this line connects your app's URLs
]
