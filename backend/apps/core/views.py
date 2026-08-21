"""
Health-check endpoint — verifies the PostGIS connection is alive.
GET /api/health/  →  {"status": "ok", "database": "connected", "postgis_version": "..."}
"""

from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    Returns HTTP 200 if the server is running and PostGIS is reachable.
    Returns HTTP 503 if the database query fails.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT PostGIS_Full_Version();")
            postgis_version = cursor.fetchone()[0]

        return Response(
            {
                "status": "ok",
                "database": "connected",
                "postgis_version": postgis_version,
            }
        )
    except Exception as exc:
        return Response(
            {
                "status": "error",
                "database": "unreachable",
                "detail": str(exc),
            },
            status=503,
        )
