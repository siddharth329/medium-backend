from django.urls import path
from .views import ImageUploadStrategy


urlpatterns = [
    path('upload/', ImageUploadStrategy.as_view(), name='image_upload_view'),
]
