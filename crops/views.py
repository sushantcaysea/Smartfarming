from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import numpy as np
import logging
import os
import json
from django.conf import settings
from .ml_model import CropModel

logger = logging.getLogger(__name__)

# Allowed agricultural ranges (must match form min/max)
INPUT_LIMITS = {
    'N': {'min': 0.0, 'max': 140.0, 'label': 'Nitrogen (N)', 'unit': 'ppm'},
    'P': {'min': 5.0, 'max': 145.0, 'label': 'Phosphorus (P)', 'unit': 'ppm'},
    'K': {'min': 5.0, 'max': 205.0, 'label': 'Potassium (K)', 'unit': 'ppm'},
    'temp': {'min': 8.0, 'max': 44.0, 'label': 'Temperature', 'unit': '°C'},
    'humidity': {'min': 14.0, 'max': 100.0, 'label': 'Humidity', 'unit': '%'},
    'ph': {'min': 3.5, 'max': 9.9, 'label': 'Soil pH', 'unit': ''},
    'rainfall': {'min': 20.0, 'max': 300.0, 'label': 'Rainfall', 'unit': 'mm'},
}


def validate_crop_inputs(raw_values):
    """Reject values outside realistic soil/climate ranges."""
    errors = []
    for key, value in raw_values.items():
        limits = INPUT_LIMITS[key]
        if value < limits['min'] or value > limits['max']:
            unit = f" {limits['unit']}" if limits['unit'] else ''
            errors.append(
                f"{limits['label']}: {value}{unit} is outside allowed range "
                f"({limits['min']}–{limits['max']}{unit})."
            )
    return errors


def get_rationale(crop, inputs, crop_ranges):
    crop_name = crop.lower().strip()
    if crop_name not in crop_ranges:
        return ["Optimal environmental threshold alignment."]
    
    crop_range = crop_ranges[crop_name]
    param_names = {
        'N': 'Nitrogen',
        'P': 'Phosphorus',
        'K': 'Potassium',
        'temp': 'Temperature',
        'humidity': 'Humidity',
        'ph': 'Soil pH',
        'rainfall': 'Rainfall'
    }
    param_units = {
        'N': ' ppm',
        'P': ' ppm',
        'K': ' ppm',
        'temp': '°C',
        'humidity': '%',
        'ph': '',
        'rainfall': ' mm'
    }
    
    reasons = []
    keys = ['N', 'P', 'K', 'temp', 'humidity', 'ph', 'rainfall']
    for key, val in zip(keys, inputs):
        p_min = crop_range[key]['min']
        p_max = crop_range[key]['max']
        unit = param_units[key]
        name = param_names[key]
        
        if p_min <= val <= p_max:
            reasons.append(f"{name}: {val}{unit} aligns with optimal range ({p_min} to {p_max}{unit})")
        else:
            reasons.append(f"{name}: {val}{unit} is outside optimal bounds ({p_min} to {p_max}{unit})")
    return reasons

def get_parameter_analysis(crop, inputs, crop_ranges):
    crop_name = crop.lower().strip()
    if crop_name not in crop_ranges:
        return []
    
    crop_range = crop_ranges[crop_name]
    param_names = {
        'N': 'Nitrogen',
        'P': 'Phosphorus',
        'K': 'Potassium',
        'temp': 'Temperature',
        'humidity': 'Humidity',
        'ph': 'Soil pH',
        'rainfall': 'Rainfall'
    }
    param_units = {
        'N': 'ppm',
        'P': 'ppm',
        'K': 'ppm',
        'temp': '°C',
        'humidity': '%',
        'ph': '',
        'rainfall': 'mm'
    }
    param_icons = {
        'N': 'flask',
        'P': 'vial',
        'K': 'atom',
        'temp': 'thermometer-half',
        'humidity': 'tint',
        'ph': 'scale-balanced',
        'rainfall': 'cloud-rain'
    }
    max_bounds = {key: info['max'] for key, info in INPUT_LIMITS.items()}
    
    analysis = []
    keys = ['N', 'P', 'K', 'temp', 'humidity', 'ph', 'rainfall']
    for key, val in zip(keys, inputs):
        p_min = crop_range[key]['min']
        p_max = crop_range[key]['max']
        unit = param_units[key]
        name = param_names[key]
        icon = param_icons.get(key, 'info-circle')
        max_b = max_bounds.get(key, 100.0)
        
        if val < p_min:
            status = 'low'
            status_text = 'Below Optimal'
            status_class = 'status-low'
        elif val > p_max:
            status = 'high'
            status_text = 'Above Optimal'
            status_class = 'status-high'
        else:
            status = 'optimal'
            status_text = 'Optimal'
            status_class = 'status-optimal'
            
        actual_percent = min(100.0, max(0.0, (val / max_b) * 100))
        min_percent = min(100.0, max(0.0, (p_min / max_b) * 100))
        max_percent = min(100.0, max(0.0, (p_max / max_b) * 100))
        optimal_width = max(1.0, max_percent - min_percent)
        
        analysis.append({
            'key': key,
            'name': name,
            'icon': icon,
            'value': round(val, 1) if key != 'ph' else round(val, 2),
            'min': p_min,
            'max': p_max,
            'unit': unit,
            'status': status,
            'status_text': status_text,
            'status_class': status_class,
            'actual_percent': round(actual_percent, 1),
            'min_percent': round(min_percent, 1),
            'max_percent': round(max_percent, 1),
            'optimal_width': round(optimal_width, 1)
        })
    return analysis

def get_simple_reason(crop, inputs, crop_ranges):
    crop_name = crop.lower().strip()
    if crop_name not in crop_ranges:
        return "it matches the overall soil and environmental profile."
    
    crop_range = crop_ranges[crop_name]
    param_names = {
        'N': 'Nitrogen',
        'P': 'Phosphorus',
        'K': 'Potassium',
        'temp': 'temperature',
        'humidity': 'humidity',
        'ph': 'soil pH',
        'rainfall': 'rainfall'
    }
    
    matching_params = []
    keys = ['N', 'P', 'K', 'temp', 'humidity', 'ph', 'rainfall']
    for key, val in zip(keys, inputs):
        p_min = crop_range[key]['min']
        p_max = crop_range[key]['max']
        if p_min <= val <= p_max:
            matching_params.append(param_names[key])
            
    if not matching_params:
        return "it represents the closest overall fit for your soil and climate combination."
    elif len(matching_params) == len(keys):
        return "all soil and environmental parameters align perfectly with its optimal growth conditions."
    else:
        if len(matching_params) > 1:
            params_str = ", ".join(matching_params[:-1]) + " and " + matching_params[-1]
        else:
            params_str = matching_params[0]
        return f"the {params_str} levels are highly compatible with its cultivation requirements."

@login_required
def crop_recommendation(request):
    rf_recommendations = None
    svm_recommendations = None
    gb_recommendations = None
    rf_primary_crop = None
    svm_primary_crop = None
    gb_primary_crop = None
    rf_primary_reason = ""
    svm_primary_reason = ""
    gb_primary_reason = ""
    consensus_agreed = False
    form_values = {key: '' for key in INPUT_LIMITS}
    
    if request.method == 'POST':
        form_values = {
            key: request.POST.get(key, '').strip()
            for key in INPUT_LIMITS
        }

        try:
            parsed = {}
            for key in INPUT_LIMITS:
                if form_values[key] == '':
                    raise ValueError(f"{INPUT_LIMITS[key]['label']} is required.")
                parsed[key] = float(form_values[key])
        except ValueError as e:
            messages.error(request, str(e) if 'required' in str(e).lower() else
                           "Invalid input values. Please enter numbers only.")
            return render(request, 'crops/recommendation.html', {
                'rf_recommendations': None,
                'svm_recommendations': None,
                'gb_recommendations': None,
                'rf_primary_crop': None,
                'svm_primary_crop': None,
                'gb_primary_crop': None,
                'rf_primary_reason': "",
                'svm_primary_reason': "",
                'gb_primary_reason': "",
                'consensus_agreed': False,
                'form_values': form_values,
            })

        range_errors = validate_crop_inputs(parsed)
        if range_errors:
            for err in range_errors:
                messages.error(request, err)
            return render(request, 'crops/recommendation.html', {
                'rf_recommendations': None,
                'svm_recommendations': None,
                'gb_recommendations': None,
                'rf_primary_crop': None,
                'svm_primary_crop': None,
                'gb_primary_crop': None,
                'rf_primary_reason': "",
                'svm_primary_reason': "",
                'gb_primary_reason': "",
                'consensus_agreed': False,
                'form_values': form_values,
            })

        try:
            raw_inputs = [
                parsed['N'],
                parsed['P'],
                parsed['K'],
                parsed['temp'],
                parsed['humidity'],
                parsed['ph'],
                parsed['rainfall'],
            ]
            
            input_data = np.array([raw_inputs])
            crop_model = CropModel()

            if not crop_model.is_loaded():
                messages.error(request, "Crop models are not loaded. Please contact the administrator.")
                return render(request, 'crops/recommendation.html', {
                    'rf_recommendations': None,
                    'svm_recommendations': None,
                    'gb_recommendations': None,
                    'rf_primary_crop': None,
                    'svm_primary_crop': None,
                    'gb_primary_crop': None,
                    'rf_primary_reason': "",
                    'svm_primary_reason': "",
                    'gb_primary_reason': "",
                    'consensus_agreed': False,
                    'form_values': form_values,
                })
            
            # RF top-5
            rf_raw = crop_model.predict_top_n(input_data, algorithm='rf', n=5)
            
            # SVM top-5
            svm_raw = crop_model.predict_top_n(input_data, algorithm='svm', n=5)

            # GB top-5
            gb_raw = crop_model.predict_top_n(input_data, algorithm='gb', n=5)
            
            # Crop ranges
            ranges_path = os.path.join(settings.BASE_DIR, 'model', 'crop_ranges.json')
            try:
                with open(ranges_path, 'r') as f:
                    crop_ranges = json.load(f)
            except Exception as e:
                logger.error(f"Error loading crop ranges JSON: {e}")
                crop_ranges = {}
                
            # Build results
            rf_recommendations = []
            for crop, conf in rf_raw:
                rf_recommendations.append({
                    'crop': crop,
                    'confidence': round(conf, 1),
                    'rationale': get_rationale(crop, raw_inputs, crop_ranges),
                    'analysis': get_parameter_analysis(crop, raw_inputs, crop_ranges)
                })
                
            svm_recommendations = []
            for crop, conf in svm_raw:
                svm_recommendations.append({
                    'crop': crop,
                    'confidence': round(conf, 1),
                    'rationale': get_rationale(crop, raw_inputs, crop_ranges),
                    'analysis': get_parameter_analysis(crop, raw_inputs, crop_ranges)
                })

            gb_recommendations = []
            for crop, conf in gb_raw:
                gb_recommendations.append({
                    'crop': crop,
                    'confidence': round(conf, 1),
                    'rationale': get_rationale(crop, raw_inputs, crop_ranges),
                    'analysis': get_parameter_analysis(crop, raw_inputs, crop_ranges)
                })
                
            if rf_recommendations:
                rf_primary_crop = rf_recommendations[0]['crop']
                rf_primary_reason = get_simple_reason(rf_primary_crop, raw_inputs, crop_ranges)
                
            if svm_recommendations:
                svm_primary_crop = svm_recommendations[0]['crop']
                svm_primary_reason = get_simple_reason(svm_primary_crop, raw_inputs, crop_ranges)

            if gb_recommendations:
                gb_primary_crop = gb_recommendations[0]['crop']
                gb_primary_reason = get_simple_reason(gb_primary_crop, raw_inputs, crop_ranges)
            
            primary_crops = [crop.lower().strip() for crop in (rf_primary_crop, svm_primary_crop, gb_primary_crop) if crop]
            if len(primary_crops) == 3 and len(set(primary_crops)) == 1:
                consensus_agreed = True
            
        except Exception as e:
            logger.error(f"Crop prediction error: {e}", exc_info=True)
            messages.error(request, f"Prediction failed: {e}")
    
    return render(request, 'crops/recommendation.html', {
        'rf_recommendations': rf_recommendations,
        'svm_recommendations': svm_recommendations,
        'gb_recommendations': gb_recommendations,
        'rf_primary_crop': rf_primary_crop,
        'svm_primary_crop': svm_primary_crop,
        'gb_primary_crop': gb_primary_crop,
        'rf_primary_reason': rf_primary_reason,
        'svm_primary_reason': svm_primary_reason,
        'gb_primary_reason': gb_primary_reason,
        'consensus_agreed': consensus_agreed,
        'form_values': form_values,
    })
