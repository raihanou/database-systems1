from django.db import models
from djongo import models


class Homes(models.Model):
    floorSpace = models.IntegerField()
    floors = models.IntegerField()
    bedRooms = models.IntegerField()
    bathRooms = models.IntegerField()
    landSize = models.IntegerField()
    yearConstructed = models.IntegerField()

    def __str__(self):
        return self.name

    @staticmethod
    def get_homes_two_floors(floor_number):
        queryset=Homes.objects.filter(floors=floor_number)
        #To print the query string
        print(queryset.query.__str__())
        return queryset

    @staticmethod
    def save_new_home():
        # Create a new Homes object with the desired values
        new_home = Homes(
            floorSpace=2000,
            floors=2,
            bedRooms=3,
            bathRooms=2,
            landSize=5000,
            yearConstructed=2022
        )
        # Save the new_home object to the database
        saved_home= new_home.save()
    
    
    
    @staticmethod
    def get_homes_sold_more_than_once():
        return
