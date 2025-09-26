from django.contrib import admin
from django.utils.html import format_html
from .models import TradingNetwork, Contact, Product


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["email", "country", "city", "street", "house_number"]
    list_filter = ["country", "city"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "model", "release_date"]
    list_filter = ["release_date"]


@admin.register(TradingNetwork)
class TradingNetworkAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "node_type",
        "supplier_link",
        "get_city",
        "debt_to_supplier",
        "created_at",
    ]
    list_filter = ["contacts__city", "node_type", "created_at"]  # Фильтр по городу
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html(
                '<a href="{}">{}</a>',
                f"/admin/electronics_retail/tradingnetwork/{obj.supplier.id}/change/",
                obj.supplier.name,
            )
        return "-"

    supplier_link.short_description = "Поставщик"

    def get_city(self, obj):
        return obj.contacts.city if obj.contacts else "-"

    get_city.short_description = "Город"

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt_to_supplier=0)
        self.message_user(request, f"Задолженность очищена для {updated} объектов")

    clear_debt.short_description = "Очистить задолженность"
