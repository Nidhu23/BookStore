from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login),
    path("login/verify/", views.verify_otp),
    path("logout/", views.logout),
]
