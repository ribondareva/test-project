from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.forms import modelformset_factory

from .forms import SparePartTypeForm, SparePartForm, AttributeForm, AttributeValueForm
from .models import SparePartType, SparePart, SparePartImage, Attribute, AttributeValue, SparePartChangeLog


class SparePartChangeLogMixin:
    """
    Логируем изменения SparePart.
    """
    # какие поля сравниваем при апдейте
    diff_fields = ("spareparttype_id", "vehicle_id", "status",)

    def _log(self, spare_part, action, field_name="", old=None, new=None):
        user = getattr(self.request, "user", None)
        SparePartChangeLog.objects.create(
            spare_part=spare_part,
            action=action,
            field_name=field_name or "",
            old_value="" if old is None else str(old),
            new_value="" if new is None else str(new),
            user=user if user and user.is_authenticated else None,
        )

    def _log_created(self, spare_part):
        self._log(spare_part, action="create")

    def _log_soft_deleted(self, spare_part):
        self._log(spare_part, action="soft_delete", field_name="is_deleted", old=False, new=True)

    def _log_field_diffs(self, old_obj, new_obj):
        for f in self.diff_fields:
            old_val = getattr(old_obj, f)
            new_val = getattr(new_obj, f)
            if old_val != new_val:
                self._log(new_obj, action="update", field_name=f, old=old_val, new=new_val)

    def _log_image_added(self, spare_part, filename):
        self._log(spare_part, action="add_image", field_name="images", new=filename)

    def _log_image_deleted(self, spare_part, image_id):
        self._log(spare_part, action="delete_image", field_name="images", old=f"id={image_id}")

    def _log_attrvalue_added(self, spare_part, attribute, value):
        self._log(spare_part, action="add_attribute", field_name=f"attribute:{attribute_id_or_name(attribute)}",
                  new=value)

    def _log_attrvalue_changed(self, spare_part, attribute, old, new):
        self._log(spare_part, action="update_attribute", field_name=f"attribute:{attribute_id_or_name(attribute)}",
                  old=old, new=new)

    def _log_attrvalue_deleted(self, spare_part, attribute, old):
        self._log(spare_part, action="delete_attribute", field_name=f"attribute:{attribute_id_or_name(attribute)}",
                  old=old)


def attribute_id_or_name(attribute):
    try:
        return getattr(attribute, "id", attribute)
    except Exception:
        return str(attribute)


class SparePartTypeCreateView(CreateView):
    model = SparePartType
    form_class = SparePartTypeForm
    template_name = "spare_part/spareparttype_form.html"

    def get_success_url(self):
        return reverse_lazy("spare_part:spareparttype_list")


class SparePartTypeUpdateView(UpdateView):
    model = SparePartType
    form_class = SparePartTypeForm
    template_name = "spare_part/spareparttype_form.html"

    def get_queryset(self):
        return SparePartType.objects.all()

    def get_success_url(self):
        return reverse_lazy("spare_part:spareparttype_list")


class SparePartTypeListView(ListView):
    model = SparePartType
    template_name = "spare_part/spareparttype_list.html"
    paginate_by = 10

    def get_queryset(self):
        return SparePartType.objects.all().order_by("name")


class SparePartTypeDeleteView(DeleteView):
    model = SparePartType
    template_name = "spare_part/spareparttype_list.html"
    success_url = reverse_lazy("spare_part:spareparttype_list")

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()
        return redirect(self.success_url)

    def get_queryset(self):
        return SparePartType.objects.all()


class AttributeCreateView(CreateView):
    model = Attribute
    form_class = AttributeForm
    template_name = "spare_part/attribute_form.html"

    def get_success_url(self):
        return reverse_lazy("spare_part:attribute_list")


class AttributeUpdateView(UpdateView):
    model = Attribute
    form_class = AttributeForm
    template_name = "spare_part/attribute_form.html"

    def get_queryset(self):
        return Attribute.objects.all()

    def get_success_url(self):
        return reverse_lazy("spare_part:attribute_list")


class AttributeListView(ListView):
    model = Attribute
    template_name = "spare_part/attribute_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Attribute.objects.all().order_by("name")


class AttributeDeleteView(DeleteView):
    model = Attribute
    template_name = "spare_part/attribute_list.html"
    success_url = reverse_lazy("spare_part:attribute_list")

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()
        return redirect(self.success_url)

    def get_queryset(self):
        return Attribute.objects.filter(is_deleted=False)


class SparePartListView(ListView):
    model = SparePart
    template_name = "spare_part/sparepart_list.html"
    paginate_by = 10

    def get_queryset(self):
        return SparePart.objects.all().order_by("id")


class SparePartDetailView(DetailView):
    model = SparePart
    template_name = "spare_part/sparepart_detail.html"

    def get_queryset(self):
        return SparePart.objects.filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        images = self.object.active_images()
        ctx["images"] = images
        ctx["has_images"] = images.exists()
        ctx["attrs"] = (
            self.object.attribute_values
            .filter(is_deleted=False)
            .select_related("attribute")
        )
        ctx["change_logs"] = self.object.changes.order_by("-created_at")[:50]
        return ctx


class SparePartCreateView(SparePartChangeLogMixin, CreateView):
    model = SparePart
    form_class = SparePartForm
    template_name = "spare_part/sparepart_form.html"
    success_url = reverse_lazy("spare_part:sparepart_list")

    def _attr_formset_factory(self, extra_rows):
        return modelformset_factory(
            AttributeValue, form=AttributeValueForm,
            extra=extra_rows, can_delete=True
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        attrs_qs = Attribute.objects.filter(is_deleted=False).order_by("name")
        initial = [{"attribute": a.id} for a in attrs_qs]
        AttrFS = self._attr_formset_factory(extra_rows=attrs_qs.count())

        if self.request.POST:
            ctx["attr_formset"] = AttrFS(self.request.POST, queryset=AttributeValue.objects.none())
        else:
            ctx["attr_formset"] = AttrFS(queryset=AttributeValue.objects.none(), initial=initial)
        return ctx

    def post(self, request, *kwargs):
        form = self.get_form()

        attrs_qs = Attribute.objects.filter(is_deleted=False)
        AttrFS = self._attr_formset_factory(extra_rows=attrs_qs.count())
        formset = AttrFS(self.request.POST, queryset=AttributeValue.objects.none())

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            self._log_created(self.object)

            for f in request.FILES.getlist("file"):
                SparePartImage.objects.create(spare_part=self.object, file=f)
                self._log_image_added(self.object, f.name)

            for f in formset.forms:
                if f.cleaned_data.get("attribute") and f.cleaned_data.get("include"):
                    av = AttributeValue.objects.create(
                        spare_part=self.object,
                        attribute=f.cleaned_data["attribute"],
                        value=f.cleaned_data.get("value", "")
                    )
                    self._log_attrvalue_added(self.object, av.attribute, av.value)

            return redirect(self.success_url)
        return self.form_invalid(form)


class SparePartUpdateView(SparePartChangeLogMixin, UpdateView):
    model = SparePart
    form_class = SparePartForm
    template_name = "spare_part/sparepart_form.html"
    success_url = reverse_lazy("spare_part:sparepart_list")

    def get_queryset(self):
        return SparePart.objects.filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        images = self.object.active_images()
        ctx["images"] = images
        ctx["has_images"] = images.exists()

        AttrFS = modelformset_factory(AttributeValue, form=AttributeValueForm, extra=0, can_delete=True)
        if self.request.POST:
            ctx["attr_formset"] = AttrFS(self.request.POST,
                                         queryset=self.object.attribute_values.filter(is_deleted=False))
        else:
            ctx["attr_formset"] = AttrFS(queryset=self.object.attribute_values.filter(is_deleted=False))
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        delete_image_id = request.POST.get("delete_image_id")
        if delete_image_id:
            updated = SparePartImage.objects.filter(
                id=delete_image_id, spare_part=self.object, is_deleted=False
            ).update(is_deleted=True)
            if updated:
                self._log_image_deleted(self.object, delete_image_id)
            return redirect(self.success_url)

        old_obj = SparePart.objects.get(pk=self.object.pk)

        form = self.get_form()
        AttrFS = modelformset_factory(AttributeValue, form=AttributeValueForm, extra=0, can_delete=True)
        formset = AttrFS(self.request.POST, queryset=self.object.attribute_values.filter(is_deleted=False))

        if form.is_valid() and formset.is_valid():
            form.save()
            new_obj = SparePart.objects.get(pk=self.object.pk)
            self._log_field_diffs(old_obj, new_obj)

            for f in request.FILES.getlist("file"):
                SparePartImage.objects.create(spare_part=self.object, file=f)
                self._log_image_added(self.object, f.name)

            for f in formset.forms:
                obj = f.save(commit=False)
                obj.spare_part = self.object
                if f.cleaned_data.get("DELETE"):
                    if not obj.is_deleted:
                        self._log_attrvalue_deleted(self.object, obj.attribute, obj.value)
                    obj.is_deleted = True
                    obj.save()
                    continue

                if obj.pk:
                    old_val = AttributeValue.objects.get(pk=obj.pk).value
                    obj.save()
                    if old_val != obj.value:
                        self._log_attrvalue_changed(self.object, obj.attribute, old_val, obj.value)
                else:
                    obj.save()
                    self._log_attrvalue_added(self.object, obj.attribute, obj.value)

            return redirect(self.success_url)
        return self.form_invalid(form)


class SparePartDeleteView(SparePartChangeLogMixin, DeleteView):
    model = SparePart
    template_name = "spare_part/sparepart_list.html"
    success_url = reverse_lazy("spare_part:sparepart_list")

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()
        self._log_soft_deleted(obj)
        return redirect(self.success_url)

    def get_queryset(self):
        return SparePart.objects.filter(is_deleted=False)
