from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import numpy as np
import logging
from .ml_model import CropModel

logger = logging.getLogger(__name__)

@login_required
def crop_recommendation(request):
    prediction = None
    
    if request.method == 'POST':
        try:
            input_data = np.array([[
                float(request.POST.get('N', 0)),
                float(request.POST.get('P', 0)),
                float(request.POST.get('K', 0)),
                float(request.POST.get('temp', 0)),
                float(request.POST.get('humidity', 0)),
                float(request.POST.get('ph', 0)),
                float(request.POST.get('rainfall', 0))
            ]])
            
            if input_data.shape != (1, 7):
                raise ValueError("Incorrect input shape")
            
            crop_model = CropModel()
            prediction = crop_model.predict(input_data)
            
        except ValueError as e:
            logger.error(f"Crop prediction error: {e}")
            messages.error(request, "Invalid input values. Please check your entries.")
        except Exception as e:
            logger.error(f"Crop prediction error: {e}", exc_info=True)
            messages.error(request, "An error occurred while processing your request.")
    
    return render(request, 'crops/recommendation.html', {
        'prediction': prediction
    })
