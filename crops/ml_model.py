import joblib
import os
from django.conf import settings

class CropModel:
    _instance = None
    _rf_model = None
    _svm_model = None
    _gb_model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CropModel, cls).__new__(cls)
            cls._load_models()
        return cls._instance
    
    @classmethod
    def _load_models(cls):
        rf_path = os.path.join(settings.BASE_DIR, 'model', 'crop_model.pkl')
        svm_path = os.path.join(settings.BASE_DIR, 'model', 'crop_svm_model.pkl')
        gb_path = os.path.join(settings.BASE_DIR, 'model', 'crop_gb_model.pkl')
        
        try:
            cls._rf_model = joblib.load(rf_path)
            print("Loaded Random Forest crop model successfully.")
        except Exception as e:
            print(f"Error loading Random Forest model: {e}")
            cls._rf_model = None
            
        try:
            cls._svm_model = joblib.load(svm_path)
            print("Loaded SVM crop model successfully.")
        except Exception as e:
            print(f"Error loading SVM model: {e}")
            cls._svm_model = None

        try:
            cls._gb_model = joblib.load(gb_path)
            print("Loaded Gradient Boosting crop model successfully.")
        except Exception as e:
            print(f"Error loading Gradient Boosting model: {e}")
            cls._gb_model = None
            
    @classmethod
    def get_model(cls, algorithm='rf'):
        if algorithm == 'gb':
            if cls._gb_model is None:
                return cls._rf_model
            return cls._gb_model
        if algorithm == 'svm':
            if cls._svm_model is None:
                # RF fallback
                return cls._rf_model
            return cls._svm_model
        return cls._rf_model
    
    @classmethod
    def predict(cls, input_data, algorithm='rf'):
        model = cls.get_model(algorithm)
        if model is None:
            raise Exception("Model not loaded")
        return model.predict(input_data)[0]
    
    @classmethod
    def predict_top_n(cls, input_data, algorithm='rf', n=5):
        model = cls.get_model(algorithm)
        if model is None:
            raise Exception("Model not loaded")
        
        probabilities = model.predict_proba(input_data)[0]
        crop_classes = model.classes_
        crop_predictions = list(zip(crop_classes, probabilities))
        crop_predictions.sort(key=lambda x: x[1], reverse=True)
        top_n_predictions = [(crop, round(prob * 100, 2)) for crop, prob in crop_predictions[:n]]
        
        return top_n_predictions

    @classmethod
    def is_loaded(cls):
        return any(model is not None for model in (cls._rf_model, cls._svm_model, cls._gb_model))
