from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from vehicle.forms import VehicleForm, VehicleTypeForm
from vehicle.models import VehicleType, Vehicle, VehicleImage


class VehicleTypeCreateView(CreateView):
    model = VehicleType
    form_class = VehicleTypeForm
    template_name = "vehicle/vehicletype_form.html"
    success_url = reverse_lazy('vehicle_types')


class VehicleTypeUpdateView(UpdateView):
    model = VehicleType
    form_class = VehicleTypeForm
    template_name = "vehicle/vehicletype_form.html"
    success_url = reverse_lazy('vehicle_types')


class VehicleTypeListView(ListView):
    model = VehicleType
    template_name = "vehicle/vehicletype_list.html"
    paginate_by = 10


class VehicleTypeDeleteView(DeleteView):
    model = VehicleType
    template_name = "vehicle/vehicletype_list.html"
    success_url = reverse_lazy("vehicle_types")

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()
        return HttpResponseRedirect(self.success_url)

    def get_queryset(self):
        return VehicleType.objects.filter(is_deleted=False)


class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicle/vehicle_form.html"
    success_url = reverse_lazy("vehicles")


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = "vehicle/vehicle_detail.html"


class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicle/vehicle_form.html"
    success_url = reverse_lazy("vehicles")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object  # чтобы работало {{ object.images.all }}
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        delete_image_id = request.POST.get("delete_image_id")
        if delete_image_id:
            try:
                image = VehicleImage.objects.get(id=delete_image_id, vehicle=self.object)
                image.is_deleted = True
                image.save()
            except ObjectDoesNotExist:
                pass
            return redirect("vehicle_update", pk=self.object.pk)

        form = self.get_form()
        if form.is_valid():
            form.save()

            for file in request.FILES.getlist("file"):
                VehicleImage.objects.create(
                    vehicle=self.object,
                    file=file
                )

            return redirect("vehicles")
        return self.form_invalid(form)


class VehicleListView(ListView):
    model = Vehicle
    template_name = "vehicle/vehicle_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        brand = self.request.GET.get("brand")
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        return queryset


class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = "vehicle/vehicle_list.html"
    success_url = reverse_lazy("vehicles")

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()
        return HttpResponseRedirect(self.success_url)

    def get_queryset(self):
        return Vehicle.objects.filter(is_deleted=False)
