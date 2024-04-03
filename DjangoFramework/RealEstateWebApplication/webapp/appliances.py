from django.db import models
from djongo import models


class Appliances(models.Model):
    modelNumber = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    maker = models.CharField(max_length=100)
    price = models.IntegerField()
    
    def __str__(self):
        return self.name
