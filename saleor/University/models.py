from django.db import models
from ..account.models import User
from django.utils import timezone
# Create your models here


class University(models.Model):
    collegeName = models.CharField(max_length=500)
    collegeURL = models.URLField(max_length=1000)
    collegeLocation = models.CharField(max_length=500)
    collegeLocationURL = models.URLField(max_length=1000)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    userPhone = models.CharField(max_length=15)
    userEmail = models.CharField(max_length=200)
    
    def __str__(self):
        return self.collegeName


class consignment(models.Model):
    university = models.ForeignKey(University,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    consignmentID = models.CharField(max_length=100,blank=False,unique=True)
    date = models.DateTimeField(auto_now_add=True)
    totalPair  =models.IntegerField()
    price = models.IntegerField()
    Shipped = 'Shipped'
    On_Route = 'On Route'
    Delivered = 'Delivered'
    state = [(Shipped, 'Shipped'),(On_Route, 'On Route'),(Delivered, 'Delivered')]
    status = models.CharField(max_length=20,choices=state,default=Shipped)
    totalCommission = models.IntegerField()

class representativePush(models.Model):
    consignment = models.ForeignKey(consignment,on_delete=models.CASCADE)
    pushMoney = models.IntegerField()