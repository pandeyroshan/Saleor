from django.db import models
from ..account.models import User
# Create your models here.


class University(models.Model):
    collegeName = models.CharField(max_length=500)
    collegeURL = models.URLField(max_length=1000)
    collegeLocation = models.CharField(max_length=500)
    collegeLocationURL = models.URLField(max_length=1000)

class CollegeRepr(models.Model):
    college = models.ForeignKey(University,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    userPhone = models.CharField(max_length=15)
    userEmail = models.CharField(max_length=200)
    userLocation = models.URLField(max_length=1000)