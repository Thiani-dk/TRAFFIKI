from django.urls import path
from . import views

urlpatterns = [
    path('vehicles/', views.get_all_vehicles, name='get_all_vehicles'),
    path('simulate/', views.simulate_import, name='simulate_import'),
    path('move-active/<int:pk>/', views.move_to_active, name='move_to_active'),
    path('delete/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),
    path('write-off/<int:pk>/', views.write_off_vehicle),
    path('download-report/', views.download_garage_report),
]