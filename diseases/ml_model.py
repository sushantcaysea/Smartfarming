import os
import numpy as np
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from PIL import Image

class DiseaseModel:
    _instance = None
    _model = None
    _validation_model = None
    _class_names = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DiseaseModel, cls).__new__(cls)
            cls._load_models()
        return cls._instance
    
    @classmethod
    def _load_models(cls):
        model_path = os.path.join(settings.BASE_DIR, 'model', 'leaf_disease_model.h5')
        data_path = os.path.join(settings.BASE_DIR, 'plant_disease_data', 'PlantVillage')
        
        try:
            cls._model = load_model(model_path)
            cls._class_names = sorted(os.listdir(data_path))
            cls._validation_model = MobileNetV2(weights='imagenet', include_top=True)
            print(f"Disease model loaded successfully with {len(cls._class_names)} classes")
        except Exception as e:
            print(f"Error loading models: {e}")
            cls._model = None
            cls._validation_model = None
            cls._class_names = []
    
    @classmethod
    def is_plant_image(cls, img_path):
        try:
            img = Image.open(img_path).convert('RGB')
            img = img.resize((224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            preds = cls._validation_model.predict(img_array, verbose=0)
            decoded = decode_predictions(preds, top=5)[0]
            
            plant_keywords = [
                'leaf', 'plant', 'tree', 'flower', 'vegetable', 'fruit',
                'mushroom', 'corn', 'broccoli', 'cucumber', 'bell_pepper',
                'strawberry', 'orange', 'lemon', 'banana', 'apple', 'grape',
                'pineapple', 'pomegranate', 'cauliflower', 'cabbage', 'lettuce',
                'artichoke', 'cardoon', 'acorn', 'buckeye', 'hip', 'ear',
                'rapeseed', 'daisy', 'pot', 'vase', 'garden'
            ]
            
            # Check top 5 predictions with lower threshold
            for pred in decoded:
                class_name = pred[1].lower()
                confidence = float(pred[2])
                
                if any(keyword in class_name for keyword in plant_keywords):
                    if confidence > 0.05:  # Lowered from 0.1 to 0.05
                        return True, confidence * 100, class_name
            
            # If no plant keywords found but confidence is low, allow it anyway
            # (MobileNet might not recognize diseased leaves well)
            top_confidence = float(decoded[0][2])
            if top_confidence < 0.3:  # If model is uncertain, allow the image
                return True, top_confidence * 100, "uncertain_classification"
            
            top_class = decoded[0][1]
            top_confidence_pct = top_confidence * 100
            return False, top_confidence_pct, top_class
            
        except Exception as e:
            print(f"Image validation error: {e}")
            # On error, allow the image through
            return True, 0, "validation_error"
    
    @classmethod
    def predict(cls, img_path):
        if cls._model is None:
            raise Exception("Model not loaded")
        
        try:
            img = image.load_img(img_path, target_size=(256, 256))
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            preds = cls._model.predict(img_array, verbose=0)
            index = np.argmax(preds)
            prediction = cls._class_names[index]
            confidence = round(100 * np.max(preds), 2)
            
            # Format the prediction for better display
            formatted_prediction = cls._format_disease_name(prediction)
            
            print(f"Prediction: {formatted_prediction}, Confidence: {confidence}%")
            print(f"Top 3 predictions:")
            top_3_indices = np.argsort(preds[0])[-3:][::-1]
            for i in top_3_indices:
                print(f"  {cls._format_disease_name(cls._class_names[i])}: {preds[0][i]*100:.2f}%")
            
            return formatted_prediction, confidence
        except Exception as e:
            print(f"Prediction error: {e}")
            raise
    
    @classmethod
    def _format_disease_name(cls, name):
        """Format disease name for better display"""
        # Replace underscores with spaces
        name = name.replace('_', ' ')
        
        # Replace double underscores that became double spaces
        name = name.replace('  ', ' - ')
        
        # Capitalize each word properly
        words = name.split()
        formatted_words = []
        
        for word in words:
            # Keep acronyms uppercase, capitalize others
            if word.isupper() and len(word) <= 3:
                formatted_words.append(word)
            else:
                formatted_words.append(word.capitalize())
        
        return ' '.join(formatted_words)
    
    @classmethod
    def is_loaded(cls):
        return cls._model is not None and cls._validation_model is not None
