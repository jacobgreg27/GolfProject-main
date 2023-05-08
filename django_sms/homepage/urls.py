from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path
from .views import LoginView

app_name = "homepage"
urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("login/", LoginView.as_view(), name="login"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
