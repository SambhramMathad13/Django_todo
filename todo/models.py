# sambh
# sambhu
from django.db import models
from django.contrib.auth.models import User

class todos(models.Model):
    title=models.CharField(max_length=20)
    desc=models.CharField(max_length=200)
    user=models.CharField(max_length=20)

    def __str__ (self):
        return self.title

# Create your models here.

