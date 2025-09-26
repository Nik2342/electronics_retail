from django.urls import path
from .views import TradingNetworkList, TradingNetworkDetail

urlpatterns = [
    path(
        "trading-networks/", TradingNetworkList.as_view(), name="trading-network-list"
    ),
    path(
        "trading-networks/<int:pk>/",
        TradingNetworkDetail.as_view(),
        name="trading-network-detail",
    ),
]
