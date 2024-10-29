from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_users, name='get_users'),
    path('divisions/', views.get_divisions, name='get_divisions'),
    path('yards/', views.get_yards, name='get_yards'),
    path('slots/', views.get_slots, name='get_slots'),
    path('structures/', views.get_structures, name='get_structures'),
    path('drivers/', views.get_drivers, name='get_drivers'),
    path('transactions/', views.get_transactions, name='get_transactions'),
    path('trucks/', views.get_trucks, name='get_trucks'),
    path('chassis/', views.get_chassis, name='get_chassis'),
    path('containers/', views.get_containers, name='get_containers'),
    path('trailers/', views.get_trailers, name='get_trailers'),
    path('maintenance/', views.get_maintenances, name='get_maintenance'),
    path('slot-updates/', views.get_slot_updates, name='get_slot_updates'),
]
