import os

allowed_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts if h.strip()]

DEBUG = os.getenv("DJANGO_DEBUG", "False").strip().lower() == "true"

 
csrf_origins_env = os.getenv("CSRF_TRUSTED_ORIGINS", "")
if csrf_origins_env:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins_env.split(",") if origin.strip()]
else:
    CSRF_TRUSTED_ORIGINS = []
    if not DEBUG:
 
        CSRF_TRUSTED_ORIGINS = [
            f"https://{h.strip()}" for h in allowed_hosts
            if h.strip() not in ("localhost", "127.0.0.1")
        ]

 
cors_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "")

if cors_origins_env:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
    CORS_ALLOW_ALL_ORIGINS = False
else:
    if DEBUG:
        CORS_ALLOW_ALL_ORIGINS = True
        CORS_ALLOWED_ORIGINS = []
    else:
        CORS_ALLOW_ALL_ORIGINS = False
        CORS_ALLOWED_ORIGINS = [
            f"https://{h.strip()}" for h in allowed_hosts
            if h.strip() not in ("localhost", "127.0.0.1")
        ]

CORS_ALLOW_CREDENTIALS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')