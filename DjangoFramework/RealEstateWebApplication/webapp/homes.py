from django.db import models
from djongo import models
from webapp.owners import Owners
from webapp.appliances import Appliances
from django.db.models import Max , Count, Q


# class Appliances(models.Model):
#     modelNumber = models.CharField(max_length=100)
#     class Meta:
#         abstract = True 

class Homes(models.Model):
    floorSpace = models.IntegerField()
    floors = models.IntegerField()
    bedRooms = models.IntegerField()
    bathRooms = models.IntegerField()
    landSize = models.IntegerField()
    yearConstructed = models.IntegerField()
    homeId = models.IntegerField(primary_key=True)
    htype = models.CharField(max_length=100)
    price = models.IntegerField()
    #owner = models.CharField(max_length=100)
    owner = models.ForeignKey("Owners", on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    preowned = models.IntegerField()
    #appliances= models.CharField(max_length=100)
    #appliances = models.EmbeddedField( model_container=Appliances,blank=True,)
    appliances = models.ForeignKey('Appliances',on_delete=models.CASCADE)
    #appliances = models.OneToOneField(Appliances, on_delete=models.CASCADE)

    def __str__(self):
        #return self.name
        return f"{self.htype} in {self.city}"
         #return f"{self.homeId}
        #appliances = self.appliances
        #return f"Homes {self.homeId}: {appliances.modelNumber}" 
        
 
    @staticmethod
    def save_new_home(floorSpace, floors, bedRooms, bathRooms, landSize, yearConstructed, homeId, htype, price, owner, city, preowned, appliances,status):  
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
        owner=owner,# Here, owner_instance is used directly
        city=city,
        preowned=preowned,
        appliances=appliances,
        status=status
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
        queryset=Homes.objects.filter(preowned__gt=1)
        #To print the query string
        print(str(queryset.query))
        return queryset
        
    
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
        
        queryset = Homes.objects.filter(city=city, preowned=1, status="available")  # Assuming preowned=1 indicates homes for sale

        if min_bedrooms is not None:
            queryset = queryset.filter(bedRooms__gte=min_bedrooms)

        if min_bathrooms is not None:
            queryset = queryset.filter(bathRooms__gte=min_bathrooms)

        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

   
    @staticmethod
    def get_owners_of_most_expensive_homes_in_city(city):
        # Step 1: Group homes by city and find the maximum price for each city.
        max_prices_per_city = Homes.objects.values('city').annotate(max_price=Max('price'))
        #, the annotate() function is used to add aggregate values to each object in a queryset.
        # Step 2: Loop through each city and retrieve the homes with the maximum price.
        expensive_homes= []
        for city_info in max_prices_per_city:
            city = city_info['city']
            max_price = city_info['max_price']
            city_expensive_homes = Homes.objects.filter(city=city, price=max_price).distinct()
            expensive_homes.extend(list(city_expensive_homes))
           #extend is used to append the list

        #return owners_of_expensive_homes_by_city
        return expensive_homes
    
    
    # @staticmethod
    # def get_homes_with_all_appliances_by_maker(maker):
    #     # Step 1: Retrieve all appliances by the specified maker
    #     appliances_by_maker = Appliances.objects.filter(maker=maker)

    #     # Step 2: Count the number of appliances by the maker
    #     num_appliances = appliances_by_maker.count()

    #     # Step 3: Retrieve homes that have all appliances by the same maker
    #     homes_with_all_appliances = Homes.objects.annotate(
    #         num_matching_appliances=Count('appliances', filter=Q(appliances__maker=maker))
    #     ).filter(num_matching_appliances=num_appliances)

    #     return homes_with_all_appliances