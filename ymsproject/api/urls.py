from django.urls import path
from . import views

urlpatterns = [
    ## users
    path('users/', views.get_users, name='get_users'),
    ## divisions
    path('divisions/', views.get_divisions, name='get_divisions'),
    ## yards
    path('yards/', views.get_yards, name='get_yards'),
    ## slots
    path('slots/', views.get_slots, name='get_slots'),
    path('slot/yard_slot_info/',views.get_yard_slot_info, name ='get_yard_slot_info'),
    # path('slot/slot_updated/',views.get_slot_updated, name ='get_slot_updated'),
    ## strucures
    path('structures/', views.get_structures, name='get_structures'),
    ## Driver
    path('drivers/', views.get_drivers, name='get_drivers'),
    path('sorted_drivers/', views.get_sorted_drivers, name='get_sorted_drivers'),
    path('create_driver/', views.create_driver, name='create_driver'),
    path('driver_details/', views.get_driver_details, name='driver_details'),
    
    ## Transaction
    path('transactions/', views.get_transactions, name='get_transactions'),
    # path('transactions/updated_transactions/', views.get_updated_transactions, name='get_updated_transactions'),
    ## Equipments
    path('equipment/updated_equipments/',views.get_updated_equipments,name='get_updated_equipments'),
    path('equipment/equipment_details/',views.get_equipment_details,name='get_equipment_details'),
    ## truck
    path('trucks/', views.get_trucks, name='get_trucks'),
    ## chassis
    path('chassis/', views.get_chassis, name='get_chassis'),
    ## containers
    path('containers/', views.get_containers, name='get_containers'),
    ## trailers
    path('trailers/', views.get_trailers, name='get_trailers'),
    ## maintaence
    path('maintenance/', views.get_maintenances, name='get_maintenance'),
    ## slot-updates
    path('slot-updates/', views.get_slot_updates, name='get_slot_updates'),
]
