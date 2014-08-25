from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.





class UserDetails(models.Model):
    email=models.EmailField(max_length=40,primary_key=True)
    password=models.CharField(max_length=40)
    hashed=models.CharField(max_length=255)
    verified=models.IntegerField()

class active(models.Model):
	aid=models.IntegerField(primary_key=True)
	active_player=models.IntegerField(default=1)

	
    
    
class UserProfile(models.Model):

    email=models.ForeignKey(UserDetails)
    first_name=models.CharField(max_length=40)
    last_name=models.CharField(max_length=40)
    CHOICES=(('M','Male'),('F','Female'),('N','Not Specified'))
    gender=models.CharField(max_length=1,choices=CHOICES)
    age=models.IntegerField()

# class pBidModel(models.Model):
# 	pId=models.IntegerField(primary_key=True)
# 	pBid=models.IntegerField(default=0)
# 	pOwner=models.CharField(max_length=100)

    
class Player(models.Model):
    pName = models.CharField(max_length=200)
    pCountry = models.CharField(max_length=100)
    pAge = models.IntegerField()
    pExpertise = models.CharField(max_length=100)
    pMatches = models.IntegerField()
    pBaseprice = models.DecimalField(max_digits = 20, decimal_places=2)
    pStatus = models.CharField(max_length=20)
    pTeam = models.CharField(max_length=20, default='DUM')
    pBid = models.DecimalField(max_digits = 20, decimal_places=2, default = 0)
    pAuctioned = models.DecimalField(max_digits=1, decimal_places=0, default = 0)
    pBatAvg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    pBallAvg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    pCatches = models.IntegerField(default=0)

    def __unicode__(self):
        return self.pName


class activePlayer(models.Model):
	aId=models.IntegerField(primary_key=True)

class Bidder(models.Model):
    email=models.EmailField(max_length=40, primary_key=True)
    password=models.CharField(max_length=40)
    start = models.IntegerField()

class Team(models.Model):
    name = models.CharField(max_length=40, primary_key = True)
    owner = models.CharField(max_length=40)

class UserPurse(models.Model):
    playersList=models.CharField(max_length=5000)
    playersBought=models.IntegerField(default=0)
    playersForeign=models.IntegerField(default=0)
    deactivated=models.IntegerField(default=0)
    money=models.IntegerField(default=600000000)
    user_data=models.ForeignKey(User)