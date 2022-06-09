from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts", null=True)
    full_name = models.CharField(max_length=250)
    relationship = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=1000)

    def __str__(self):
          return self.full_name