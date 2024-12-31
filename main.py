import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import InMemoryUploadedFile
from ultralytics import YOLO
from PIL import Image
import secrets

# Django Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    SECRET_KEY=secrets.token_urlsafe(50),
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    INSTALLED_APPS=[],
)

# Load YOLO Model
MODEL_PATH = '/Users/atulalexander/Desktop/agrithontest/best.pt'
model = YOLO(MODEL_PATH)

@csrf_exempt
def predict_coconut(request):
    if request.method == 'POST':
        # Get the uploaded image
        image_file: InMemoryUploadedFile = request.FILES.get('image')
        if not image_file:
            return JsonResponse({'error': 'No image uploaded'}, status=400)

        # Open the image and process it
        try:
            image = Image.open(image_file)
            results = model.predict(source=image, save=False, conf=0.25)

            # Extract prediction results
            predictions = results[0].boxes
            if len(predictions) == 0:
                return JsonResponse({'prediction': 'No coconut detected'})

            maturity = predictions[0].cls  # Get the prediction class
            # Swap the labels here - if model predicts mature (1), we return tender and vice versa
            if float(maturity) == 1:  # Convert to float for comparison
                label = 'tender'
            else:
                label = 'mature'

            response = JsonResponse({'prediction': label})
            response["Access-Control-Allow-Origin"] = "*"
            return response
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Handle GET request with a simple HTML form for testing
    if request.method == 'GET':
        return HttpResponse('''
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Coconut Prediction</h2>
            <form action="/predict/" method="post" enctype="multipart/form-data">
                <input type="file" name="image" accept="image/*">
                <input type="submit" value="Predict">
            </form>
        </body>
        </html>
        ''')

    return JsonResponse({'error': 'Invalid request'}, status=400)

# URL Patterns
urlpatterns = [
    path('predict/', predict_coconut, name='predict_coconut'),
]

# Run the Server
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)

    if 'runserver' in sys.argv:
        execute_from_command_line([sys.argv[0], 'runserver', '127.0.0.1:8000'])
    else:
        execute_from_command_line(sys.argv)