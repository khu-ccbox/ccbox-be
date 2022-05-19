from django.urls import path, include
from folder import views


urlpatterns = [
    path("", views.FolderAPI.as_view()),
    path("<int:folderID>", views.FolderIdAPI.as_view()),
]