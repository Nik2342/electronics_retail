from rest_framework import generics, permissions
from .models import TradingNetwork
from .serializers import TradingNetworkSerializer


class IsActiveEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active


class TradingNetworkList(generics.ListCreateAPIView):
    queryset = TradingNetwork.objects.all()
    serializer_class = TradingNetworkSerializer
    permission_classes = [IsActiveEmployee]

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get("country")
        if country:
            queryset = queryset.filter(contacts__country__icontains=country)
        return queryset


class TradingNetworkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TradingNetwork.objects.all()
    serializer_class = TradingNetworkSerializer
    permission_classes = [IsActiveEmployee]
