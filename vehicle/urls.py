from django.urls import path
from vehicle.views import (
    VehicleTypeCreateView, VehicleTypeUpdateView, VehicleTypeListView, VehicleTypeDeleteView,
    VehicleCreateView, VehicleDetailView, VehicleUpdateView, VehicleListView, VehicleDeleteView
)

urlpatterns = [
    path("vehicle-types/create/", VehicleTypeCreateView.as_view(), name="vehicle_type_create"),
    path("vehicle-types/<int:pk>/", VehicleTypeUpdateView.as_view(), name="vehicle_type_update"),
    path("vehicle-types/", VehicleTypeListView.as_view(), name="vehicle_types"),
    path("vehicle-types/<int:pk>/delete/", VehicleTypeDeleteView.as_view(), name="vehicle_type_delete"),

    path("vehicles/create/", VehicleCreateView.as_view(), name="vehicle_create"),
    path("vehicles/<int:pk>/", VehicleDetailView.as_view(), name="vehicle_detail"),
    path("vehicles/<int:pk>/edit/", VehicleUpdateView.as_view(), name="vehicle_update"),
    path("vehicles/", VehicleListView.as_view(), name="vehicles"),
    path("vehicles/<int:pk>/delete/", VehicleDeleteView.as_view(), name="vehicle_delete"),
]
