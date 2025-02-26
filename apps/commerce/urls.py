from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.commerce.views import ProductListView, TransactionViewSet

router = DefaultRouter()
router.register(r'products', ProductListView)
router.register(r'vending', TransactionViewSet, basename='vending')

urlpatterns = [
    path('', include(router.urls)),
]
