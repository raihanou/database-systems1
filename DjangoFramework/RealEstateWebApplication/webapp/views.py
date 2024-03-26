import pymongo


from django.shortcuts import render
from webapp.owners import Owners
from webapp.homes import Homes
from webapp.agents import Agents
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse


def home(request):
    context={}
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["CSI5450"]
    collection = db["webapp_homes"]

    # Retrieve data from MongoDB
    data_from_mongo1 = collection.find({}, {"_id": 0, "owner": 1}) # Assuming you want to retrieve the "name" field
    # data_from_mongo = collection.distinct('owner') # Assuming you want to retrieve the "name" field
    # print(data_from_mongo)
    data_from_mongo = set(item['owner'] for item in data_from_mongo1)
    


    return render(request, "webapp/index.html", {'data_from_mongo': data_from_mongo})
    
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
         #owner = request.POST.get('owner')
         owner = request.POST.get('owner')  # Retrieve owner's name
         city = request.POST.get('city')
         preowned = request.POST.get('preowned')
         appliances = request.POST.get('appliances')
    Homes.save_new_home(flrSpace,flrs,bdRooms,bthRooms,landSize,yearConstd,hid,htyp,price,owner,city,preowned,appliances)
         
    return render(request, "webapp/index.html",context)

@csrf_exempt
def move_from_sale_to_owned(request):
    context={}
    
        
    return render(request, "webapp/index.html",context)

@csrf_exempt
def make_home_owner(request):
    context={}
    
       
    return render(request, "webapp/index.html",context)

@csrf_exempt
def filter_homes(request):
    context={}
   
       
    return render(request, "webapp/index.html",context)


@csrf_exempt
def list_homes_owned_by_owner_in_city(request):
    context = {}
    if request.method == 'POST':
        owner_name = request.POST.get('owner')
        city_name = request.POST.get('city')
        homes = Homes.get_homes_owned_by_owner_in_city(owner_name, city_name)
        context['homes'] = homes
    return render(request, "webapp/homes_list.html", context)

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
    return render(request, 'home_search_results.html', context) 


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
            query_result=Homes.get_homes_two_floors(2)

        elif selected_option == 'q2':
            query_result=Homes.get_homes_two_floors(2)
            
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
            query_result=Homes.get_homes_two_floors(2)
        
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
    
    
        
