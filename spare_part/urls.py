from django.urls import path
from . import views

app_name = 'spare_part'

urlpatterns = [
    path("types/", views.SparePartTypeListView.as_view(), name="spareparttype_list"),
    path("types/create/", views.SparePartTypeCreateView.as_view(), name="spareparttype_create"),
    path("types/<int:pk>/", views.SparePartTypeUpdateView.as_view(), name="spareparttype_update"),
    path("types/<int:pk>/delete/", views.SparePartTypeDeleteView.as_view(), name="spareparttype_delete"),

    path("attributes/", views.AttributeListView.as_view(), name="attribute_list"),
    path("attributes/create/", views.AttributeCreateView.as_view(), name="attribute_create"),
    path("attributes/<int:pk>/", views.AttributeUpdateView.as_view(), name="attribute_update"),
    path("attributes/<int:pk>/delete/", views.AttributeDeleteView.as_view(), name="attribute_delete"),

    path("", views.SparePartListView.as_view(), name="sparepart_list"),
    path("create/", views.SparePartCreateView.as_view(), name="sparepart_create"),
    path("<int:pk>/", views.SparePartDetailView.as_view(), name="sparepart_detail"),
    path("<int:pk>/edit/", views.SparePartUpdateView.as_view(), name="sparepart_update"),
    path("<int:pk>/delete/", views.SparePartDeleteView.as_view(), name="sparepart_delete"),
]
