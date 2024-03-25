from . import views
from django.urls import path

urlpatterns = [
    path("",views.home, name="home"),
    path("twoFloors",views.preDefinedQuery, name="preDefinedQuery"),
    path("preDefinedQuery",views.preDefinedQuery, name="preDefinedQuery"),
    path("addAgent",views.addAgent, name="addAgent"),
    path("addHome",views.addHome, name="addHome"),
    path("move_from_sale_to_owned",views.move_from_sale_to_owned, name="move_from_sale_to_owned"),
    path("make_home_owner",views.make_home_owner, name="make_home_owner"),
    path("filter_homes",views.filter_homes, name="filter_homes"),
    
]


