from django.shortcuts import render
from webapp.owners import Owners
from webapp.homes import Homes
from webapp.agents import Agents
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings



def home(request):
    context={}
    return render(request, "webapp/index.html",context)
    
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
def preDefinedQuery(request):
    context={}
    
    if request.method == 'POST':
        selected_option = request.POST.get('selected_option')

        if selected_option == 'q1':
            query_result=Homes.get_homes_two_floors(2)

        elif selected_option == 'q2':
            query_result=Homes.get_homes_two_floors(2)
            
        elif selected_option == 'q3':
            query_result=Homes.get_homes_two_floors(2)
    
        elif selected_option == 'q4':
            query_result=Homes.get_People_With_Apts_Mansions()
            
        elif selected_option == 'q5':
            query_result=Homes.get_homes_two_floors(2)
            
        elif selected_option == 'q6':
            query_result=Homes.get_homes_two_floors(2)
        
        elif selected_option == 'q7':
            query_result = Homes.get_most_expensive_home_for_owner()
        
        elif selected_option == 'q8':
            query_result = Homes.get_homes_below_price_in_given_city()
        
        elif selected_option == 'q9':
            query_result = Homes.find_homes_for_sale()
           
        else: 
            query_result=Homes.get_homes_two_floors(2)
    
    return render(request, "webapp/jsondisplaypage.html", {'documents': query_result})
    
    
        
