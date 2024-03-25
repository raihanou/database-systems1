from django.db import models
from djongo import models
#from webapp.owners import Owners
#from webapp.appliances import Appliances


class Homes(models.Model):
    floorSpace = models.IntegerField()
    floors = models.IntegerField()
    bedRooms = models.IntegerField()
    bathRooms = models.IntegerField()
    landSize = models.IntegerField()
    yearConstructed = models.IntegerField()
    homeId = models.IntegerField()
    htype = models.CharField(max_length=100)
    price = models.IntegerField()
    owner = models.CharField(max_length=100)
    #owner = models.ForeignKey(Owners, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    preowned = models.IntegerField()
    appliances= models.CharField(max_length=100)
    #appliances = models.ForeignKey(Appliances,on_delete=models.CASCADE)
    

    def __str__(self):
        #return self.name
        return f"{self.htype} in {self.city}"

 
    @staticmethod
   
    def save_new_home(floorSpace, floors, bedRooms, bathRooms, landSize, yearConstructed, homeId, htype, price, owner, city, preowned, appliances):
    # Create a new Homes object with the desired values
     new_home = Homes(
        floorSpace=floorSpace,
        floors=floors,
        bedRooms=bedRooms,
        bathRooms=bathRooms,
        landSize=landSize,
        yearConstructed=yearConstructed,
        homeId=homeId,
        htype=htype,
        price=price,
        owner=owner,
        city=city,
        preowned=preowned,
        appliances=appliances,
    )
        # Save the new_home object to the database
     saved_home= new_home.save()
     return saved_home
    
   
 
 
    @staticmethod
    def get_homes_two_floors(floor_number):
        queryset=Homes.objects.filter(floors=floor_number)
        print(queryset.query.__str__())
        return queryset

    
        #To print the query string
    @staticmethod
    def get_homes_sold_more_than_once():
        return
    
    @staticmethod
    def get_most_expensive_home_for_owner(name):
        queryset = Homes.objects.filter(owner=name)
        queryset=queryset.order_by('-price')
        most_expensive_home = queryset.first()
        print(queryset.query.__str__())  # Print the generated SQL query
        return queryset.filter(pk=most_expensive_home.pk)
    
    @staticmethod
    def get_homes_owned_by_owner_in_city(owner_name, city_name):
        queryset = Homes.objects.filter(owner=owner_name, city=city_name)
        return queryset
    
    @staticmethod
    def get_People_With_Apts_Mansions():
        queryset = Homes.objects.filter(htype="Apartments").filter(htype="Mansions").distinct()
        return queryset
    
    @staticmethod
    def get_homes_below_price_in_given_city(city, price):
        queryset = Homes.objects.filter(city=city, price__lt=price)
        return queryset
    
    @staticmethod
    def find_homes_for_sale(city, min_bedrooms=None, min_bathrooms=None, max_price=None):
        
        queryset = Homes.objects.filter(city=city, preowned=1)  # Assuming preowned=1 indicates homes for sale

        if min_bedrooms is not None:
            queryset = queryset.filter(bedRooms__gte=min_bedrooms)

        if min_bathrooms is not None:
            queryset = queryset.filter(bathRooms__gte=min_bathrooms)

        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

   
    