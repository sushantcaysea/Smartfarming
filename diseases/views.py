from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image, UnidentifiedImageError
import os
import logging
from .ml_model import DiseaseModel

logger = logging.getLogger(__name__)

ALLOWED_CONTENT_TYPES = {
    'image/jpeg',
    'image/jpg',
    'image/png',
    'image/webp',
}


def allowed_extension(filename):
    if not filename or '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_IMAGE_EXTENSIONS


def is_valid_image_upload(uploaded_file):
    # Image validation
    if not uploaded_file or not allowed_extension(uploaded_file.name):
        return False, "Invalid file type. Please upload a JPG, PNG, or WebP image."

    content_type = (getattr(uploaded_file, 'content_type', '') or '').lower().strip()
    if content_type and content_type not in ALLOWED_CONTENT_TYPES:
        return False, "Invalid file type. Only image files are allowed."

    max_bytes = getattr(settings, 'MAX_IMAGE_UPLOAD_BYTES', 8 * 1024 * 1024)
    if uploaded_file.size and uploaded_file.size > max_bytes:
        return False, "Image is too large. Please upload a file under 8 MB."

    try:
        uploaded_file.seek(0)
        with Image.open(uploaded_file) as img:
            img.verify()
        uploaded_file.seek(0)
        with Image.open(uploaded_file) as img:
            img.load()
            if img.format not in ('JPEG', 'PNG', 'WEBP'):
                return False, "Unsupported image format. Please use JPG, PNG, or WebP."
        uploaded_file.seek(0)
    except (UnidentifiedImageError, OSError, ValueError):
        return False, "Uploaded file is not a valid image."

    return True, ""


@login_required
def disease_detection(request):
    prediction = None
    confidence = None
    img_url = None
    
    if request.method == 'POST' and request.FILES.get('leaf'):
        file = request.FILES['leaf']
        ok, error_message = is_valid_image_upload(file)
        if not ok:
            messages.error(request, error_message)
            return redirect('diseases:detection')

        file_path = None
        try:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)

            disease_model = DiseaseModel()
            is_valid, val_confidence, detected_class = disease_model.is_plant_image(file_path)

            if not is_valid:
                label = detected_class.replace('_', ' ').strip()
                if detected_class in ('validation_error', 'validator_unavailable'):
                    detail = "We could not verify this as a plant leaf."
                elif label:
                    detail = (
                        f"It looks more like “{label.title()}” "
                        f"({val_confidence:.1f}% ImageNet confidence) than a leaf."
                    )
                else:
                    detail = "This does not look like a plant leaf."
                messages.error(
                    request,
                    f"Upload rejected: {detail} "
                    f"Please upload a clear photo of a plant leaf."
                )
                if os.path.exists(file_path):
                    os.remove(file_path)
                return redirect('diseases:detection')

            prediction, confidence = disease_model.predict(file_path)
            img_url = fs.url(filename)

        except UnidentifiedImageError:
            messages.error(request, "Uploaded file is not a valid image.")
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            return redirect('diseases:detection')
        except Exception as e:
            logger.error(f"Disease prediction error: {e}", exc_info=True)
            messages.error(request, "Error processing image. Please try again.")
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            return redirect('diseases:detection')
    elif request.method == 'POST':
        messages.error(request, "Please choose an image file to analyze.")
        return redirect('diseases:detection')
    
    return render(request, 'diseases/detection.html', {
        'prediction': prediction,
        'confidence': confidence,
        'img_path': img_url
    })
