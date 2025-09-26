from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Contact(models.Model):
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=255, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class TradingNetwork(models.Model):
    FACTORY = "factory"
    RETAIL = "retail"
    IE = "ie"

    NODE_TYPES = (
        (FACTORY, "Завод"),
        (RETAIL, "Розничная сеть"),
        (IE, "Индивидуальный предприниматель"),
    )

    name = models.CharField(max_length=255, verbose_name="Название")
    node_type = models.CharField(
        max_length=10, choices=NODE_TYPES, verbose_name="Тип звена"
    )
    contacts = models.OneToOneField(
        Contact, on_delete=models.CASCADE, verbose_name="Контакты"
    )
    products = models.ManyToManyField(Product, verbose_name="Продукты")
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик",
        related_name="children",
    )
    debt_to_supplier = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Задолженность перед поставщиком",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def clean(self):
        errors = {}

        if self.node_type == self.FACTORY and self.supplier is not None:
            errors["supplier"] = "Завод не может иметь поставщика"

        if self.supplier and self.supplier.id == self.id:
            errors["supplier"] = "Объект не может быть своим собственным поставщиком"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_node_type_display()}: {self.name}"

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
