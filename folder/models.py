from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child', null=True)
    name = models.CharField(max_length=100, blank=False)
    color = models.PositiveIntegerField(null=True)