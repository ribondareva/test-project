from django.db import models


class VehicleType(models.Model):
    name = models.CharField("Название типа", max_length=20)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    is_deleted = models.BooleanField("Логическое удаление", default=False)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    reg_number = models.CharField("Регистрационный номер", max_length=20)
    brand = models.CharField("Марка ", max_length=20)
    date_purchase = models.DateField("Дата покупки")
    vehicle_type = models.ForeignKey(VehicleType, verbose_name="Тип техники", on_delete=models.CASCADE)
    mileage = models.DecimalField("Пробег", max_digits=10, decimal_places=2)
    OPERATION_STATUS_CHOICES = (
        ("work", "в работе"),
        ("wait", "простой"),
        ("repair", "ремонт"),
    )
    operation_status = models.CharField("Статус", max_length=10, choices=OPERATION_STATUS_CHOICES)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    is_deleted = models.BooleanField("Логическое удаление", default=False)

    def __str__(self):
        return f"{self.reg_number} ({self.brand})"


class VehicleImage(models.Model):
    file = models.ImageField(upload_to='vehicle_images/')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Фото для {self.vehicle.reg_number}"
