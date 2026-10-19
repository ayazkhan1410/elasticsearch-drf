from django.contrib import admin
from django.urls import include, path

from product.views import SearchPageView

urlpatterns = [
    path("", SearchPageView.as_view(), name="search-page"),
    path("admin/", admin.site.urls),
    path("api/products/", include("product.urls")),
]
