from rest_framework.response import Response
from rest_framework.views import APIView


class HealthAPIView(APIView):
    """Simple health check so we can confirm the API is running."""

    def get(self, request):
        return Response({"status": "ok", "app": "product"})


class RetrieveProductDataView(APIView):
    """Retrieve product data from the database."""

    def get(self, request):
        search = request.GET.get("search")
        if not search:
            return Response({"error": "Search query is required"}, status=400)
