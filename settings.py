# In your project's __init__.py (or a custom middleware file)
import logging
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
class CORSTestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        self.logger.info("CORS Test Middleware is running!")
        response = self.get_response(request)
        return response

#settings.py
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'your_project.CORSTestMiddleware', # Add your custom middleware here
]