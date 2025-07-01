from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.utils import timezone
from .models import Url


@extend_schema(
    request={"application/json": {"type": "object", "properties": {
        "original_url": {"type": "string"}
    }}},
    responses={201: {"type": "object", "properties": {
        "shortened_url": {"type": "string"}
    }}}
)
class ShortenUrlView(APIView):
    def post(self, request):
        try:
            original_url = request.data.get("original_url")
            if not original_url:
                return Response({'error': 'original_url is required'}, status=status.HTTP_400_BAD_REQUEST)

            existing = Url.objects.filter(original_url=original_url).first()
            if existing:
                return Response({'shortened_url': f"/api/{existing.shortened_code}"})

            new_url = Url.objects.create_url(original_url)

            return Response({'shortened_url': f"/api/{new_url.shortened_code}"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            import traceback
            print("🔥 EXCEPTION:")
            print(traceback.format_exc())
            return Response({'error': 'Internal server error'}, status=500)


@extend_schema(
    parameters=[OpenApiParameter("shortened_code", str, OpenApiParameter.PATH)],
    responses={302: None, 404: {"type": "object", "properties": {
        "error": {"type": "string"}
    }}}
)
class RedirectToOriginalView(APIView):
    def get(self, request, shortened_code):
        try:
            url = Url.objects.get(shortened_code=shortened_code)
            url.clicks += 1
            url.last_accessed = timezone.now()
            url.save(update_fields=["clicks", "last_accessed"])
            return Response({'original_url': url.original_url}, status=status.HTTP_302_FOUND)
        except Url.DoesNotExist:
            raise NotFound("Shortened URL not found")


@extend_schema(
    parameters=[OpenApiParameter("shortened_code", str, OpenApiParameter.PATH)],
    responses={200: {"type": "object", "properties": {
        "original_url": {"type": "string"},
        "shortened_code": {"type": "string"},
        "clicks": {"type": "integer"},
        "created_at": {"type": "string", "format": "date-time"},
        "last_accessed": {"type": ["string", "null"], "format": "date-time"}
    }}}
)
class UrlStatsView(APIView):
    def get(self, request, shortened_code):
        try:
            url = Url.objects.get(shortened_code=shortened_code)
            return Response({
                "original_url": url.original_url,
                "shortened_code": url.shortened_code,
                "clicks": url.clicks,
                "created_at": url.created_at,
                "last_accessed": url.last_accessed
            })
        except Url.DoesNotExist:
            raise NotFound("Shortened URL not found")
