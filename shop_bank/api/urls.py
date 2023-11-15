from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PingView, CityViewSet, StreetViewSet, ShopModelViewSet

router = DefaultRouter()

router.register('city', CityViewSet, basename='city')
router.register(r'city/(?P<city_id>\d+)/street', StreetViewSet,
                basename='street')
router.register('shop', ShopModelViewSet, basename='shop')

urlpatterns = [
    path('', PingView.as_view(), name='ping'),
    path('', include(router.urls))
    ]
