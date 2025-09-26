from rest_framework import viewsets, permissions
from .models import TradingNetwork, Contact, Product
from .serializers import TradingNetworkSerializer


class IsActiveEmployee(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active


class TradingNetworkViewSet(viewsets.ModelViewSet):

    queryset = TradingNetwork.objects.all()
    serializer_class = TradingNetworkSerializer
    permission_classes = [IsActiveEmployee]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по стране (требование задания)
        country = self.request.query_params.get("country")
        if country:
            queryset = queryset.filter(contacts__country__icontains=country)

        return queryset
