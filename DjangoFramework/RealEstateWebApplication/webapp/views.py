from django.shortcuts import render
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
        id = request.POST.get('AgentID')
        name = request.POST.get('Name')
        cRate = request.POST.get('CommissionRate')
        company = request.POST.get('Company')
    query_result=Agents.save_new_agent(id,name,cRate,company)
    return render(request, "webapp/index.html",context)

@csrf_exempt
def addHome(request):
    context={}
    if request.method == 'POST':
        # Retrieve field values from the form data
        id = request.POST.get('AgentID')
        name = request.POST.get('Name')
        cRate = request.POST.get('CommissionRate')
        company = request.POST.get('Company')
    query_result=Homes.save_new_home()
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
            query_result=Homes.get_homes_two_floors(2)
            
        elif selected_option == 'q5':
            query_result=Homes.get_homes_two_floors(2)
            
        else: 
            query_result=Homes.get_homes_two_floors(2)
    
    return render(request, "webapp/jsondisplaypage.html", {'documents': query_result})
    
