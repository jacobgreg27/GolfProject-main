"""django_sms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from homepage.views import HomePageView
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("smsApp.urls")),
    path("", include("homepage.urls")), 
]
# hander404 = 'smsApp.views.error_404_view'
# hander500 = 'smsApp.views.error_500_view'
# hander403 = 'smsApp.views.error_403_view'
# hander400 = 'smsApp.views.error_400_view'
