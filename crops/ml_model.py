import joblib
import os
from django.conf import settings

class CropModel:
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CropModel, cls).__new__(cls)
            cls._load_model()
        return cls._instance
    
    @classmethod
    def _load_model(cls):
        model_path = os.path.join(settings.BASE_DIR, 'model', 'crop_model.pkl')
        try:
            cls._model = joblib.load(model_path)
        except Exception as e:
            print(f"Error loading crop model: {e}")
            cls._model = None
    
    @classmethod
    def predict(cls, input_data):
        if cls._model is None:
            raise Exception("Model not loaded")
        return cls._model.predict(input_data)[0]
    
    @classmethod
    def is_loaded(cls):
        return cls._model is not None
