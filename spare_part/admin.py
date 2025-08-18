from django.contrib import admin
from .models import SparePartType, SparePart, SparePartImage, Attribute, AttributeValue


@admin.register(SparePartType)
class SparePartTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_deleted", "created_at", "updated_at")
    list_filter = ("is_deleted",)
    search_fields = ("name",)


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ("id", "spareparttype", "vehicle", "status", "is_deleted", "created_at")
    list_filter = ("status", "is_deleted", "spareparttype")
    search_fields = ("vehicle__reg_number",)


@admin.register(SparePartImage)
class SparePartImageAdmin(admin.ModelAdmin):
    list_display = ("id", "spare_part", "is_deleted", "created_at")


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "unit", "data_type", "is_deleted")


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("id", "spare_part", "attribute", "value", "is_deleted")
    list_filter = ("attribute",)
