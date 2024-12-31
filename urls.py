# urls.py (in your project directory)
from django.contrib import admin
from django.urls import path
from . import main  # Import your main.py file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', main.predict_coconut, name='predict_coconut'),  # Directly from main.py
]