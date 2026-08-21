"""
Root URL configuration for FoodBridge.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # Health check
    path("api/", include("apps.core.urls")),
    # App-specific API routes (wire up as you build them)
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/listings/", include("apps.listings.urls")),
    path("api/matching/", include("apps.matching.urls")),
    path("api/dispatch/", include("apps.dispatch.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
