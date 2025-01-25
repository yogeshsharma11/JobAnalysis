from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    population = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()