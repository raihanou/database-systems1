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
    def get_most_expensive_home_for_owner():
        # queryset = Homes.objects.filter(owner=owner_name)
        # queryset=queryset.order_by('-price')
        queryset=Homes.objects.order_by('-price')
        most_expensive_home = queryset.first()
        print(queryset.query.__str__())  # Print the generated SQL query
        return queryset.filter(price=most_expensive_home.price)
    @staticmethod
    def get_homes_owned_by_owner_in_city(owner_name, city_name):
        queryset = Homes.objects.filter(owner=owner_name, city=city_name)
        return queryset
    
    @staticmethod
    def get_homes_filtered(owner, city, price, home_t):
        filtered_homes = Homes.objects.all()
        if owner:
            filtered_homes = filtered_homes.filter(owner=owner)

        if city:
            filtered_homes = filtered_homes.filter(city=city)

        if home_t:
            filtered_homes = filtered_homes.filter(htype=home_t )

        if price:
            filtered_homes = filtered_homes.filter(price__lte=price)

        # queryset = Homes.objects.filter(owner=owner).filter(city=city).filter(htype=home_t).filter(price__lt=price)
        # print(queryset)
        return filtered_homes
    
    @staticmethod
    
    def get_People_With_Apts_Mansions():
        apartments = set(Homes.objects.filter(htype="Apartments").values_list("owner", flat=True).distinct())
        mansions = set(Homes.objects.filter(htype="Mansions").values_list("owner", flat=True).distinct())
        print(type(apartments))
        print(mansions)
        # Find the intersection of owners who own both types
        users_with_both_types = apartments.intersection(mansions)
        # Retrieve homes owned by users with both types'
        homes = Homes.objects.filter(owner__in=users_with_both_types).filter(htype__in=['Apartments', 'Mansions'])

        return homes
    
    @staticmethod
    def get_homes_below_price_in_given_city(city, price):
        # city='Troy'
        # price = 222
        queryset = Homes.objects.filter(city=city, price__lt=int(price))
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

   
    