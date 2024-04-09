from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:account_id>/balance/", views.balance, name="balance"),
]