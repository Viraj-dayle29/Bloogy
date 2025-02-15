from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    username = models.CharField(max_length=50,default="raju")
    date = models.DateTimeField(default=timezone.now)
    full_name = models.CharField(max_length=50,default="Unknown")
    summ = models.TextField(null=True, blank=True)