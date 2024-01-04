from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jobTitle = models.CharField(max_length=32, blank=True)
    company = models.CharField(max_length=32, blank=True)
