from django.db import models
from djongo import models


class Owners(models.Model):
    ssn = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    dependents = models.IntegerField()
    income = models.IntegerField()
    age = models.IntegerField()
    profession = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name









