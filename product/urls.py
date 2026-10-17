from django.urls import path

from product.views import HealthAPIView

urlpatterns = [
    path("health/", HealthAPIView.as_view(), name="product-health"),
]
