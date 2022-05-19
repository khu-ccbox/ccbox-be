from django.urls import path
from .view import AccountView, SignView

urlpatterns = [
    path('', AccountView.as_view()),
    path('/sign-up', AccountView.as_view()),
    path('/sign-in', SignView.as_view()),
]
