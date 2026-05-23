from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [('customer', 'Customer'), ('admin', 'Admin')]

    email       = models.EmailField(unique=True)
    phone       = models.CharField(max_length=20, blank=True)
    role        = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    def is_admin_user(self):
        return self.role == 'admin'

    def __str__(self):
        return self.email
