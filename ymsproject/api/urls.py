from django.urls import path
from . import views
from . import git

urlpatterns = [
    # Git Management Endpoint
    path('git/pull', git.git_pull, name='git-pull'),  # POST
    
    # Live Map Endpoints
    path('livemap/yards',views.get_yards, name="get_yards"),
    path('livemap/yard-info', views.get_yard_slot_info, name='get_yard_slot_info'),
    path('livemap/updated', views.get_updated_equipments, name='get_updated_equipments'),
    path('livemap/is-updated', views.get_slot_isupdated, name='get_slot_isupdated'),
    path('livemap/current-state', views.current_slot_state, name='current_slot_state'),
    path('livemap/process-list', views.get_livemap_not_end, name='get_livemap_not_end'),
    path('livemap/set-destination-slot', views.set_destination_slot, name='set_destination_slot'),
    
    
    # Driver Endpoints
    path('driver/sorted', views.get_sorted_drivers, name='get_sorted_drivers'),
    path('driver/create', views.create_driver, name='create_driver'),
    path('driver/details-driver', views.get_driver_details, name='driver_details'),
    path('driver/history', views.driver_transaction_history, name='driver_history'),
    
    # transaction Endpoints
    path('transaction/sorted', views.get_sorted_transactions, name='get_sorted_transactions'),
    # path('transaction/create', views.create_transaction, name='create_transaction'),
    # path('transaction/details-transaction', views.get_transaction_details, name='transaction_details'),
    # path('transaction/history', views.transaction_transaction_history, name='transaction_history'),
    # path('transaction/update-state', views.update_transaction_state, name='update_transaction_state'),
    
    # Equipment Endpoints
    path('equipment/equipment-details', views.get_equipment_details, name='get_equipment_details'),
    path('equipment/sorted', views.get_sorted_equipments, name='get_sorted_equipments'),
    path('equipment/history', views.equipment_transaction_history, name='equipment_transaction_history'),  # Equipment transaction history
    path('livemap/chassis-flip', views.chassis_flip_sql, name='chassis_flip'),
    path('livemap/move', views.move_equipment, name='move_equipment'),
    path('livemap/connect', views.connect_container, name='connect_container'),
    path('livemap/disconnect', views.disconnect_container, name='disconnect_container'),
    
    # User Endpoints
    path('user/signup', views.user_signup, name='user_signup'),
    path('user/login', views.user_login, name='user_login'),

    # TMS Endpoints
    path('TMS/current_map', views.get_current_map, name='get_current_map'),

    # Dashboard Endpoint
    path('dashboard/recent-transaction', views.get_recent_transaction, name='get_recent_transaction'),
    path('dashboard/weather', views.get_weather, name='get_weather'),
    path('dashboard/update-weather', views.update_weather, name='update_weather'),
    path('dashboard/today_transaction', views.get_today_summary, name='get_today_transaction'),
    path('dashboard/processing-transaction',views.get_processing_transaction,name='get_processing_transaction'),
    
    # Server Status Endpoint
    path('server-status/', views.server_status, name='server_status'),
]
