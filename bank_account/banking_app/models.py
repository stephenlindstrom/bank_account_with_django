from django.db import models

class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=None, decimal_places=2, default=0)
