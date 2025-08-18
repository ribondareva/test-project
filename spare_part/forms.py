from django import forms
from .models import SparePartType, SparePart, Attribute, AttributeValue


class SparePartTypeForm(forms.ModelForm):
    class Meta:
        model = SparePartType
        fields = ["name"]


class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ["spareparttype", "vehicle", "status"]


class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ["name", "unit", "data_type"]


class AttributeValueForm(forms.ModelForm):
    include = forms.BooleanField(required=False, initial=True, label="Добавить")  # флажок

    class Meta:
        model = AttributeValue
        fields = ["attribute", "value"]
