from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.utils.crypto import get_random_string
from smsApp.views import member_detail
from homepage.views import HomePageView
from .views import scanner_view


# Generate a random string of 20 characters
random_str = get_random_string(length=20)

# Append the random string to the login URL
from django.conf import settings

app_name = "smsApp"
urlpatterns = [
    path("", HomePageView.as_view(), name="page"),
    path("login/" + random_str + "/", views.login_page, name="login-page"),
    path("register/", views.userregister, name="register-page"),
    path("save_register", views.save_register, name="register-user"),
    path("user_login", views.login_user, name="login-user"),
    path("home/", views.home, name="home-page"),
    path("logout", views.logout_user, name="logout"),
    path("profile", views.profile, name="profile-page"),
    path("update_password", views.update_password, name="update-password"),
    path("update_profile", views.update_profile, name="update-profile"),
    path("users", views.users, name="user-page"),
    path("manage_user", views.manage_user, name="manage-user"),
    path("manage_user/<int:pk>", views.manage_user, name="manage-user-pk"),
    path("save_user", views.save_user, name="save-user"),
    path("delete_user/<int:pk>", views.delete_user, name="delete-user"),
    path("groups", views.groups, name="group-page"),
    path("manage_group", views.manage_group, name="manage-group"),
    path("manage_group/<int:pk>", views.manage_group, name="manage-group-pk"),
    path("view_group/<int:pk>", views.view_group, name="view-group-pk"),
    path("save_group", views.save_group, name="save-group"),
    path("delete_group/<int:pk>", views.delete_group, name="delete-group"),
    path("members", views.members, name="member-page"),
    path("manage_member", views.manage_member, name="manage-member"),
    path("manage_member/<int:pk>", views.manage_member, name="manage-member-pk"),
    # path('view_member',views.view_member,name='view-member'),
    path("view_member/<int:pk>/", views.view_member, name="view-member"),
    path("view_member/scanner.html", scanner_view, name="scanner-view"),
    path("save_member", views.save_member, name="save-member"),
    path("delete_member/<int:pk>", views.delete_member, name="delete-member"),
    path("group_member/", views.per_group, name="group-member"),
    path("member", member_detail, name="member_detail"),
    # path('view_member'+ random_str + '/',views.view_details,name='scanned-code'),
    path("scanner", views.view_scanner, name="scanner"),
    path("scanner_view/", views.scanner_view, name="scanner-view"),
]


