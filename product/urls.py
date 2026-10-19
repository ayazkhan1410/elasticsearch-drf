from django.urls import path

from product.views import HealthAPIView, RetrieveProductDataView


urlpatterns = [
    path("health/", HealthAPIView.as_view(), name="product-health"),
    path("", RetrieveProductDataView.as_view(), name="product-data"),
]
