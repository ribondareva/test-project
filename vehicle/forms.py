from django import forms
from .models import Vehicle, VehicleType


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['reg_number', 'brand', 'date_purchase', 'vehicle_type', 'mileage', 'operation_status']
        widgets = {
            'date_purchase': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ['name']
