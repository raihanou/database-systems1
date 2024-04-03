from unicodedata import name
import pymongo


from django.shortcuts import render , get_object_or_404
from webapp.appliances import Appliances
from webapp.owners import Owners
from webapp.homes import Homes
from webapp.agents import Agents
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse , HttpResponseNotFound



def home(request):
    context={}
    owner_value = context.get('owner', None)
    if owner_value is not None:
        pass
    else:
        # Connect to MongoDB and retrieve data
     client = pymongo.MongoClient("mongodb://localhost:27017/")
     db = client["CSI5450"]
     collection = db["webapp_homes"]

    # Retrieve data from MongoDB
    data_from_mongo1 = collection.find({}, {"_id": 0, "owner_id": 1}) 
    data_from_mongo = set(item['owner_id'].title() for item in data_from_mongo1)
    
    # data_from_mongo = collection.distinct('owner')
    
    data_from_mongo1 = collection.find({}, {"_id": 0, 'city':1}) # Assuming you want to retrieve the "name" field
    city_name = set(item['city'].title() for item in data_from_mongo1)
    
    collection2 = db["webapp_agents"]
    data_from_mongo2 = collection2.find({}, {"_id": 0, "name": 1}) 
    agent_name = set(item['name'].title() for item in data_from_mongo2)
    


    return render(request, "webapp/index.html", {'data_from_mongo': data_from_mongo, "agents":agent_name, 'city':city_name})
    
@csrf_exempt    
def addAgent(request):
    context={}
    if request.method == 'POST':
        # Retrieve field values from the form data
        aid = request.POST.get('AgentID')
        name = request.POST.get('Name')
        cRate = request.POST.get('CommissionRate')
        company = request.POST.get('Company')
    Agents.save_new_agent(aid,name,cRate,company)
    return render(request, "webapp/index.html",context)

@csrf_exempt
def addHome(request):
    context={}
    if request.method == 'POST':
         # Retrieve field values from the form data
         flrSpace = request.POST.get('floorSpace')
         flrs = request.POST.get('floors')
         bdRooms = request.POST.get('bedRooms')
         bthRooms = request.POST.get('bathRooms')
         landSize = request.POST.get('landSize')
         yearConstd = request.POST.get('homeYear')
         hid = request.POST.get('homeId')
         htyp = request.POST.get('homeType')
         price = request.POST.get('homePrice')
         status= request.POST.get('status')
         #owner = request.POST.get('owner')
         owner = request.POST.get('owner')  # Retrieve owner's name
         #owner_instance=get_object_or_404(Owners, ssn=owner)
         city = request.POST.get('city')
         preowned = request.POST.get('preowned', "off")=='on'
         appliances = request.POST.get('appliances')
    try:
         owner=get_object_or_404(Owners, ssn=owner)
    except Owners.DoesNotExist:
         context['error_message'] = "Owner not found. Please check the entered name."
    try:
         appliances=get_object_or_404(Appliances, modelNumber=appliances)
    except Appliances.DoesNotExist:
         context['error_message'] = "Owner not found. Please check the entered name."
    
    Homes.save_new_home(flrSpace,flrs,bdRooms,bthRooms,landSize,yearConstd,hid,htyp,price,owner,city,preowned,appliances,status)
         
    return render(request, "webapp/index.html",context)

@csrf_exempt
def move_from_sale_to_owned(request):
    context={}
    if request.method == 'POST':
        homeId = request.POST.get('homeId')
        new_owner_id = request.POST.get('owner')
        
        # Retrieve the home object
        home = get_object_or_404(Homes, homeId=homeId)
        
        # Check if the home is currently available for sale
        if home.status == 'available':
            try:
                # Retrieve the new owner object
                new_owner = Owners.objects.get(ssn=new_owner_id)
                
                # Update home status to 'owned'
                home.status = 'owned'
                
                # Assign the new owner to the home
                home.owner = new_owner
                
                # Save changes to the home object
                home.save()
                
                return HttpResponse("Home moved to owned list successfully.")
            except Owners.DoesNotExist:
                return HttpResponse("New owner does not exist", status=404)
        else:
            return HttpResponse("Home is not available for sale", status=400)

    return HttpResponse("Invalid request", status=400)
    
    
        

@csrf_exempt
def make_home_owner(request):
    context={}
    if request.method == 'POST':
        
    # hid = request.POST.get('homeId')
    # owner = request.POST.get('owner')
        homeId = request.POST.get('homeId')
        new_owner_id = request.POST.get('owner')
        try:
            new_owner = Owners.objects.get(ssn=new_owner_id)
        except Owners.DoesNotExist:
            ownername = request.POST.get('ownername')
            owner_age = request.POST.get('owner_age')
            owner_profession = request.POST.get('owner_profession')
            if ownername:
                          new_owner = Owners.objects.create(
                ssn=new_owner_id,
                name=ownername,
                age=owner_age,
                profession=owner_profession
            )
            else:
                return HttpResponse("Owner's name is required", status=400)

        try:
            # Fetch the Home instance to update
            #homeId = Homes.objects.get(homeId=homeId)
            homeId = get_object_or_404(Homes,homeId=homeId)

            # Update the owner of the home
            homeId.owner = new_owner
            homeId.status = "owned" # Assuming you want to mark the home as owned if it wasn't already
            homeId.save()

            # Return a success response
            return HttpResponse("Home owner updated successfully.")

        except Homes.DoesNotExist:
            return HttpResponse("Home not found", status=404)

        except Owners.DoesNotExist:
            return HttpResponse("Owner not found", status=404)

    else:
        # Return an error response if the request method is not POST
        return HttpResponse("Method not allowed", status=405)


      
    
@csrf_exempt
def filter_homes(request):
    context={}
   
       
    return render(request, "webapp/index.html",context)


@csrf_exempt
def list_homes_owned_by_owner_in_city(request):
    context = {}
    if request.method == 'POST':
        city_name = request.POST.get('city')
        homes = Homes.get_homes_owned_by_owner_in_city(owner_name, city_name)
        owner_name = request.POST.get('owner')
        context['homes'] = homes
    return render(request, "webapp/jsondisplaypage.html", context)

@csrf_exempt
def search_homes(request):
    city = request.GET.get('city')
    min_bedrooms = request.GET.get('min_bedrooms')
    min_bathrooms = request.GET.get('min_bathrooms')
    max_price = request.GET.get('max_price')

    homes = Homes.find_homes_for_sale(city, min_bedrooms, min_bathrooms, max_price)
    
    context = {
        'homes': homes
    }
    return render(request, 'webapp/jsondisplaypage.html', context) 


@csrf_exempt    
def searchQuery(request):
    context = {}
    agent=None
    home_t=None
    # if request.method == 'POST':
    if request.POST.get('city-select')!=None:
        city=request.POST.get('city-select')
    if request.POST.get('price-select')!=None:
        price=request.POST.get('price-select')
    if request.POST.get('owner-select')!=None:
        owner=request.POST.get('owner-select')
    if request.POST.get('agent-select')!=None:
        agent=request.POST.get('agent-select')
    if request.POST.get('home-type-select')!=None:
        home_t=request.POST.get('home-type-select')
    
    # city='Troy'
    # price = 222
    print(city)
    query_result = Homes.get_homes_filtered(owner, city, price, home_t)
    
    return render(request, "webapp/jsondisplaypage.html", {'documents': query_result})

      
@csrf_exempt    
def preDefinedQuery(request):
    context={}

    if request.method == 'POST':
        selected_option = request.POST.get('query')

        if selected_option == 'q1':
            query_result=Homes.get_homes_sold_more_than_once()
            
        elif selected_option == 'q2':
            maker = request.POST.get('maker')  # Retrieve the 'maker' value from the POST request
            homes_with_all_appliances = Homes.get_homes_with_all_appliances_by_maker(maker)
            return render(request, 'webapp/jsondisplaypage.html', {'homes': homes_with_all_appliances, 'maker': maker})


        elif selected_option == 'q3':
            query_result=Homes.get_homes_two_floors(2)
    
        elif selected_option == 'q4':
            query_result=Homes.get_People_With_Apts_Mansions()
            homes_data = []
            for home in query_result:
                home_info = {
                    'id': home.homeId,
                    'type': home.htype
                }
                homes_data.append(home_info)
            print(homes_data)
            # query_result = homes_data
            # homes_data = [{'id': home.homeId, 'type': home.htype} for home in query_result1]
            # query_result=JsonResponse({"homes":homes_data})

            
        elif selected_option == 'q5':
            query_result=Homes.get_homes_two_floors(2)
            
        elif selected_option == 'q6':
            city=request.POST.get('city')
            query_result = Homes.get_owners_of_most_expensive_homes_in_city(city)
            print(city)
            
            
        
        elif selected_option == 'q7':
            query_result = Homes.get_most_expensive_home_for_owner()
        
        elif selected_option == 'q8':
            city=request.POST.get('city-select')
            price=request.POST.get('price-select')
            query_result = Homes.get_homes_below_price_in_given_city(city, price)
        
        elif selected_option == 'q9':
            query_result = Homes.find_homes_for_sale()          
        else: 
            query_result=Homes.get_homes_two_floors(2)
    
    return render(request, "webapp/jsondisplaypage.html", {'documents': query_result})
    
    
        
