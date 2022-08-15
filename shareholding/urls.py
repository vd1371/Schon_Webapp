from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'shareholding'

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'shareholdinginfo', views.ShareholdingInfoViewSet, basename='shareholdinginfo')

urlpatterns = [
    path('', include(router.urls)),
]