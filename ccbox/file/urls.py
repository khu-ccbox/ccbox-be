from django.urls import path
from file import views

urlpatterns = [
    path('files', views.Files.as_view()),
    path('files/<int:file_id>', views.Files_id.as_view()),
]