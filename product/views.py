from django.views.generic import TemplateView
from elasticsearch_dsl import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from product.documents import ProductDocument
from product.serializer import ProductDocumentSerializer
from utils.elasticsearch import escape_wildcard


class SearchPageView(TemplateView):
    """Browser UI for testing product search against the API."""

    template_name = "product/search.html"


class HealthAPIView(APIView):
    """Simple health check so we can confirm the API is running."""

    def get(self, request):
        return Response({"status": "ok", "app": "product"})


class RetrieveProductDataView(APIView):
    """Retrieve product data from Elasticsearch (supports partial typing)."""

    def get(self, request):
        search = (request.query_params.get("search") or "").strip()
        if not search:
            return Response({"error": "Search query is required"}, status=400)

        wildcard = f"*{escape_wildcard(search.lower())}*"
        query = Q(
            "bool",
            should=[
                Q(
                    "multi_match",
                    query=search,
                    fields=["product_name^2", "description"],
                    fuzziness="AUTO",
                    type="best_fields",
                ),
                Q(
                    "match_phrase_prefix",
                    product_name={"query": search, "max_expansions": 50},
                ),
                Q(
                    "match_phrase_prefix",
                    description={"query": search, "max_expansions": 50},
                ),
                Q(
                    "wildcard",
                    product_name={"value": wildcard, "case_insensitive": True},
                ),
                Q(
                    "wildcard",
                    description={"value": wildcard, "case_insensitive": True},
                ),
            ],
            minimum_should_match=1,
        )

        products = (
            ProductDocument.search()
            .query(query)
            .extra(size=10)
            .execute()
        )

        serializer = ProductDocumentSerializer(products, many=True)
        return Response({
            "message": "Product data retrieved successfully",
            "products": serializer.data,
        })
