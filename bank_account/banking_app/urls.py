from django.contrib.auth import views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:account_id>/balance/", views.balance, name="balance"),
    path("register/", views.register, name="register"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path('signup/', views.signup, name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
]