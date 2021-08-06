from rest_framework import routers
from .views import LicenseViewSet

license_router = routers.DefaultRouter()
license_router.register(r'', LicenseViewSet)
