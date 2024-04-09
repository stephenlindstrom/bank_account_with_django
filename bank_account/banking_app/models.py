from django.db import models

class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return self.first_name + " " + self.last_name
