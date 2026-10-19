from rest_framework.response import Response
from rest_framework.views import APIView

from elasticsearch_dsl import Q

from product.documents import ProductDocument
from product.serializer import ProductDocumentSerializer


class HealthAPIView(APIView):
    """Simple health check so we can confirm the API is running."""

    def get(self, request):
        return Response({"status": "ok", "app": "product"})


class RetrieveProductDataView(APIView):
    """Retrieve product data from the database."""

    def get(self, request):
        products = []

        search = request.query_params.get("search")
        if not search:
            return Response({"error": "Search query is required"}, status=400)

        products = ProductDocument.search().query(
            Q("multi_match", query=search, fields=[
                "product_name", "description"])
        ).extra(size=5).execute()

        serializer = ProductDocumentSerializer(products, many=True)
        return Response({
            "message": "Product data retrieved successfully",
            "products": serializer.data,
        })
