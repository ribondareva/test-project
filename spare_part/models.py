from django.db import models
from sorl.thumbnail import ImageField
from vehicle.models import Vehicle


class SparePartType(models.Model):
    name = models.CharField("Название типа", max_length=50)
    image = ImageField("Изображение", upload_to="spare_part_types/", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    is_deleted = models.BooleanField("Удалено", default=False)

    class Meta:
        verbose_name = "Тип запчасти"
        verbose_name_plural = "Типы запчастей"

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField("Название", max_length=100, default="Например, Диаметр")
    unit = models.CharField("Единица измерения", max_length=20, blank=True, default="мм, кг, л и т. п.")
    data_type = models.CharField("Тип данных", max_length=20, default="Например, string")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    is_deleted = models.BooleanField("Удалено", default=False)

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

    def __str__(self):
        return self.name


class AttributeTemplate(models.Model):
    """Набор атрибутов для типа запчасти."""
    spare_part_type = models.ForeignKey(
        SparePartType, on_delete=models.CASCADE, related_name="attribute_templates", verbose_name="Тип запчасти"
    )
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="templates", verbose_name="Атрибут"
    )
    is_required = models.BooleanField("Обязательный", default=False)
    default_value = models.CharField("Значение по умолчанию", max_length=255, blank=True)

    class Meta:
        unique_together = ("spare_part_type", "attribute")
        verbose_name = "Шаблон атрибута"
        verbose_name_plural = "Шаблоны атрибутов"


class SparePart(models.Model):
    STATUS_CHOICES = (
        ("installed", "Установлено"),
        ("stock", "На складе"),
        ("repair", "В ремонте"),
        ("wait_repair", "Ожидает ремонт"),
    )

    spareparttype = models.ForeignKey(
        SparePartType, on_delete=models.CASCADE, related_name="parts", verbose_name="Тип запчасти"
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="spare_parts", verbose_name="Техника"
    )
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="stock")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    is_deleted = models.BooleanField("Удалено", default=False)

    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"

    def __str__(self):
        base = self.spareparttype.name
        return f"{base} → {self.vehicle.reg_number}" if self.vehicle_id else f"{base} (склад)"

    def active_images(self):
        return self.images.filter(is_deleted=False)


class SparePartImage(models.Model):
    file = ImageField("Файл", upload_to="sparepart_images/")
    spare_part = models.ForeignKey(
        SparePart, on_delete=models.CASCADE, related_name="images", verbose_name="Запчасть"
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    is_deleted = models.BooleanField("Удалено", default=False)

    class Meta:
        verbose_name = "Изображение запчасти"
        verbose_name_plural = "Изображения запчастей"


class AttributeValue(models.Model):
    spare_part = models.ForeignKey(
        SparePart, on_delete=models.CASCADE, related_name="attribute_values", verbose_name="Запчасть"
    )
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="values", verbose_name="Атрибут"
    )
    value = models.CharField("Значение", max_length=255, blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    is_deleted = models.BooleanField("Удалено", default=False)

    class Meta:
        unique_together = ("spare_part", "attribute")
        verbose_name = "Значение атрибута"
        verbose_name_plural = "Значения атрибутов"


class SparePartChangeLog(models.Model):
    spare_part = models.ForeignKey(
        SparePart, on_delete=models.CASCADE, related_name="changes", verbose_name="Запчасть"
    )
    action = models.CharField("Действие", max_length=50)
    field_name = models.CharField("Поле", max_length=50, blank=True)
    old_value = models.TextField("Старое значение", blank=True)
    new_value = models.TextField("Новое значение", blank=True)
    user = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь"
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Лог изменения запчасти"
        verbose_name_plural = "Логи изменений запчастей"
