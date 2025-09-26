from rest_framework import serializers
from .models import TradingNetwork, Contact, Product


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class TradingNetworkSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    contacts = ContactSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)

    class Meta:
        model = TradingNetwork
        fields = [
            "id",
            "name",
            "node_type",
            "level",
            "contacts",
            "products",
            "supplier",
            "supplier_name",
            "debt_to_supplier",
            "created_at",
        ]
        read_only_fields = ["debt_to_supplier"]

    def get_level(self, obj):
        """Вычисление уровня иерархии"""
        if obj.supplier is None:
            return 0

        # Защита от циклических ссылок
        visited = set()
        current = obj.supplier
        level = 1

        while current is not None:
            if current.id in visited:
                break
            visited.add(current.id)
            if current.supplier is None:
                return level
            current = current.supplier
            level += 1

        return level

    def update(self, instance, validated_data):
        if "debt_to_supplier" in validated_data:
            raise serializers.ValidationError(
                {"debt_to_supplier": "Обновление задолженности запрещено через API"}
            )
        return super().update(instance, validated_data)
