from django.urls import path
from . import views

urlpatterns = [
    ## Live Map Endpoints
    path('livemap/yard-info', views.get_yard_slot_info, name='get_yard_slot_info'),
    path('livemap/updated', views.get_updated_equipments, name='get_updated_equipments'),
    path('livemap/is-updated', views.get_slot_isupdated, name='get_slot_isupdated'),
    path('livemap/current-state', views.current_slot_state, name='current_slot_state'),
    
    ## Driver Endpoints
    path('driver/sorted', views.get_sorted_drivers, name='get_sorted_drivers'),
    path('driver/create', views.create_driver, name='create_driver'),
    path('driver/details-driver', views.get_driver_details, name='driver_details'),
    path('driver/history', views.driver_transaction_history, name='driver_history'),
    
    ## Equipment Endpoints
    path('equipment/equipment-details', views.get_equipment_details, name='get_equipment_details'),
    path('equipment/sorted', views.get_sorted_equipments, name='get_sorted_equipments'),
    
    ## User Endpoints
    path('user/signup', views.user_signup, name='user_signup'),
    path('user/login', views.user_login, name='user_login'),

    ## Additional Endpoints
    
]
