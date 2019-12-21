from django.db import models
from ..account.models import User
from django.utils import timezone
# Create your models here


class University(models.Model):
    collegeName = models.CharField(max_length=500)
    collegeURL = models.URLField(max_length=1000)
    collegeLocation = models.CharField(max_length=500)
    collegeLocationURL = models.URLField(max_length=1000)
    
    def __str__(self):
        return self.collegeName

class representative(models.Model):
    College = models.ForeignKey(University,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contactNo = models.CharField("Contact No", max_length=15)
    
    def __str__(self):
        return self.user.email


class consignment(models.Model):
    university = models.ForeignKey(University,on_delete=models.CASCADE)
    representative = models.ForeignKey(representative, on_delete=models.CASCADE)
    consignmentID = models.CharField(max_length=100,blank=False,unique=True)
    date = models.DateTimeField(auto_now_add=True)
    totalPair  =models.IntegerField()
    price = models.IntegerField()
    Processing = 'Processing'
    Shipped = 'Shipped'
    On_Route = 'On Route'
    Delivered = 'Delivered'
    state = [(Shipped, 'Shipped'),(On_Route, 'On Route'),(Delivered, 'Delivered'),(Processing, 'Processing')]
    status = models.CharField(max_length=20,choices=state,default=Shipped)
    totalCommission = models.IntegerField(blank=True)
    commissionPercentage = models.PositiveIntegerField("Commission Percentage")
    totalPaid = models.IntegerField(default=0)

class representativePush(models.Model):
    consignment = models.ForeignKey(consignment,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    pushMoney = models.IntegerField()
    Initiated = 'Initiated'
    Approved = 'Approved'
    state = [(Initiated, 'Initiated'),(Approved,'Approved'),]
    status = models.CharField(max_length=20,choices=state,default=Initiated)