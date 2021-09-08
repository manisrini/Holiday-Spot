from django.db import models
# from django.contrib.auth.models import User
import datetime
from django.contrib.auth import get_user_model
User=get_user_model()



# Create your models here.
class Location(models.Model):
    city = models.CharField(max_length=1000, unique=True)
    state = models.CharField(max_length=1000,default='')
    country = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=2083, unique=True)
    description = models.TextField(default='', unique=True)




    def __str__(self):
        return self.city




class Review(models.Model):
    comment = models.CharField(max_length=1000)
    author = models.ForeignKey(User,on_delete=models.CASCADE,default="author_id")
    rating = models.IntegerField(default=5)
    location=models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    currentdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

class Visited(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="user_id")
    location=models.ForeignKey(Location,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.location.city



class Search(models.Model):
    query = models.CharField(max_length=1000)

class FeedBack(models.Model):
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length = 100)
    feedback = models.CharField(max_length = 1000)

    def __str__(self):
        return self.email
# Create your models here.
