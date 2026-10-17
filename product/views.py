from rest_framework.response import Response
from rest_framework.views import APIView


class HealthAPIView(APIView):
    """Simple health check so we can confirm the API is running."""

    def get(self, request):
        return Response({"status": "ok", "app": "product"})
