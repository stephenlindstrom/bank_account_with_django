from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("<int:account_id>/balance/", views.balance, name="balance"),
    path("register/", views.register, name="register"),
    path("registered/", views. registered, name="registered"),
]