"""
Local development settings.
Reads from backend/.env — never commit the actual .env file.
"""

import environ
from pathlib import Path

# Point environ at the .env file sitting next to manage.py
env = environ.Env()
environ.Env.read_env(Path(__file__).resolve().parent.parent.parent / ".env")

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Relaxed CORS for local dev
CORS_ALLOW_ALL_ORIGINS = True

# Django Debug Toolbar can be added here later
# INSTALLED_APPS += ["debug_toolbar"]
