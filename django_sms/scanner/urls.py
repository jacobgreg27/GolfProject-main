from django.urls import path
from .views import ScannerView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "scanner"
urlpatterns = [
    path("scanner/", ScannerView, name="scanner"),
    path("qr-code/", views.generate_qr_code, name="generate_qr_code"),
    # other URL patterns...
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
