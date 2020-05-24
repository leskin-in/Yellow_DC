from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import IndexView, fp_upload, fp_photo


urlpatterns = [
    path('', IndexView.as_view()),
    path('upload/', fp_upload),
    path('photo/<slug:id>/', fp_photo),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
