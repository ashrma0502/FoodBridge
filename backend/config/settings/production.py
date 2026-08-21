"""
Production settings.
All secrets MUST come from environment variables — never hardcode them here.
"""

from .base import *  # noqa: F401, F403

DEBUG = False

# In production, set ALLOWED_HOSTS via environment variable
# e.g. ALLOWED_HOSTS=foodbridge.example.com

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
