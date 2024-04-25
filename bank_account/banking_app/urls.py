from django.contrib.auth import views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('transactions/', views.transactions, name='transactions'),
    path('signup-complete/', views.signup_complete, name='signup_complete'),
]