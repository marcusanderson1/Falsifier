from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class SearchCriteria(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    listofkeywords = models.CharField(max_length= 255, default = None)
    searchURL = models.CharField(max_length= 500, default = None)
    isCurrentSearch = models.BooleanField()
    DateCreated = models.DateTimeField( default = datetime.datetime.now)
    DateUpdated = models.DateTimeField(default = datetime.datetime.now)
    
class Person(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    dob = models.DateTimeField()
    gender = models.CharField(max_length= 1, default = None)
    DateCreated = models.DateTimeField( default = datetime.datetime.now)
    DateUpdated = models.DateTimeField(default = datetime.datetime.now)

class Results(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    searchCriteria = models.ForeignKey(SearchCriteria, on_delete=models.CASCADE)
    DateCreated = models.DateTimeField( default = datetime.datetime.now)
    DateUpdated = models.DateTimeField(default = datetime.datetime.now)


class Search(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    listofkeywords = models.CharField(max_length= 255, default = None)
    submittedURL = models.CharField(max_length= 500, default = None)
    isCurrentSearch = models.BooleanField(default=None)
    DateCreated = models.DateTimeField( default = datetime.datetime.now)

class SearchKeywordResults(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    keyword = models.CharField(max_length = 50, default = None)
    keywordCount = models.IntegerField()
    DateCreated = models.DateTimeField( default = datetime.datetime.now)

class SearchResults(models.Model):#Thisis the grouped up totals
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    sumOfKeywords = models.IntegerField(default=None)
    totalWordCount = models.IntegerField(default=None)
    keywordOccurence = models.DecimalField(max_digits=5 , decimal_places=3, )
    DateCreated = models.DateTimeField( default = datetime.datetime.now)

class AlexaResults(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    globalRank = models.IntegerField(default=None)
    countryRank = models.IntegerField(default=None)
    BounceRate = models.DecimalField(default=None, decimal_places=3, max_digits=19)
    DailyPageViews = models.IntegerField(default=None)
    DailyTimeSpent = models.IntegerField(default=None)
    SearchVisits = models.DecimalField(default=None, decimal_places=3,max_digits=19)
    DateCreated = models.DateTimeField( default = datetime.datetime.now)
    
