from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import UnidentifiedImageError
import os
import logging
from .ml_model import DiseaseModel

logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_IMAGE_EXTENSIONS

@login_required
def disease_detection(request):
    prediction = None
    confidence = None
    img_url = None
    
    if request.method == 'POST' and request.FILES.get('leaf'):
        file = request.FILES['leaf']
        
        if file and allowed_file(file.name):
            try:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_path = fs.path(filename)
                
                disease_model = DiseaseModel()
                is_valid, val_confidence, detected_class = disease_model.is_plant_image(file_path)
                
                if not is_valid:
                    messages.error(
                        request,
                        f"⚠️ This doesn't appear to be a plant leaf image. "
                        f"Detected: {detected_class.replace('_', ' ').title()} "
                        f"({val_confidence:.1f}% confidence). "
                        f"Please upload a clear image of a plant leaf."
                    )
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    return redirect('diseases:detection')
                
                prediction, confidence = disease_model.predict(file_path)
                img_url = fs.url(filename)
                
            except UnidentifiedImageError:
                messages.error(request, "Uploaded file is not a valid image.")
                return redirect('diseases:detection')
            except Exception as e:
                logger.error(f"Disease prediction error: {e}", exc_info=True)
                messages.error(request, "Error processing image. Please try again.")
                return redirect('diseases:detection')
        else:
            messages.error(request, "Invalid file type. Please upload an image file.")
            return redirect('diseases:detection')
    
    return render(request, 'diseases/detection.html', {
        'prediction': prediction,
        'confidence': confidence,
        'img_path': img_url
    })
