import os
import numpy as np
from django.conf import settings
from tensorflow.keras.models import load_model
# pyrefly: ignore [missing-import]
from tensorflow.keras.preprocessing import image
# pyrefly: ignore [missing-import]
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from PIL import Image

class DiseaseModel:
    _instance = None
    _model = None
    _validation_model = None
    _class_names = None

    # Leaf signals
    LEAF_KEYWORDS = (
        'leaf', 'plant', 'tree', 'flower', 'vine', 'fern',
        'rapeseed', 'daisy', 'cardoon', 'artichoke',
        'broccoli', 'cauliflower', 'cabbage', 'lettuce', 'brussels',
        'head_cabbage', 'corn', 'maize', 'cucumber', 'bell_pepper',
        'zucchini', 'butternut', 'squash', 'fig',
        'garden', 'greenhouse', 'lawn', 'picket_fence',
    )

    ANIMAL_KEYWORDS = (
        'dog', 'cat', 'bird', 'fish', 'shark', 'whale', 'frog', 'turtle',
        'lizard', 'snake', 'spider', 'tick', 'beetle', 'butterfly', 'ant',
        'bee', 'fly', 'cockroach', 'scorpion', 'snail', 'slug',
        'fox', 'wolf', 'bear', 'lion', 'tiger', 'leopard', 'cheetah',
        'monkey', 'ape', 'gorilla', 'chimp', 'orangutan', 'baboon',
        'horse', 'zebra', 'donkey', 'cow', 'ox', 'buffalo', 'bison',
        'sheep', 'ram', 'goat', 'pig', 'hog', 'boar', 'deer', 'camel',
        'llama', 'rabbit', 'hare', 'hamster', 'guinea', 'squirrel',
        'mouse', 'rat', 'hedgehog', 'koala', 'wombat', 'kangaroo',
        'elephant', 'rhino', 'hippo', 'otter', 'seal', 'walrus',
        'penguin', 'ostrich', 'duck', 'goose', 'swan', 'chicken', 'cock',
        'hen', 'peacock', 'parrot', 'owl', 'eagle', 'hawk', 'macaw',
        'terrier', 'spaniel', 'poodle', 'retriever', 'hound', 'collie',
        'shepherd', 'husky', 'malamute', 'pug', 'boxer', 'chihuahua',
        'bulldog', 'mastiff', 'dane', 'ridgeback', 'samoyed', 'pomeranian',
        'corgi', 'kelpie', 'vizsla', 'weimaraner', 'setter', 'pointer',
        'bernese', 'appenzeller', 'entlebucher', 'rottweiler', 'doberman',
        'dalmatian', 'affenpinscher', 'papillon', 'maltese', 'shi',
        'pekinese', 'shih', 'basset', 'beagle', 'bluetick', 'coonhound',
        'whippet', 'greyhound', 'saluki', 'komondor', 'kuvasz', 'schipperke',
        'keeshond', 'briard', 'standard_poodle', 'Mexican_hairless',
        'tabby', 'tiger_cat', 'persian', 'siamese', 'egyptian', 'cougar',
        'lynx', 'leopard', 'jaguar', 'snow_leopard', 'meerkat', 'mongoose',
    )

    # Hard reject
    HARD_NON_PLANT_KEYWORDS = (
        'website', 'menu', 'book', 'envelope', 'comic', 'puzzle', 'jigsaw',
        'screen', 'monitor', 'laptop', 'notebook', 'keyboard',
        'computer_mouse', 'remote', 'joystick', 'cellphone', 'iPod', 'television',
        'chocolate', 'candy', 'bagel', 'pretzel', 'waffle', 'pizza',
        'hotdog', 'hamburger', 'burrito', 'guacamole', 'trifle',
        'ice_cream', 'ice_lolly', 'french_loaf',
        'brick', 'tile', 'quonset', 'window_screen', 'washer', 'stove',
        'wallet', 'packet', 'binding', 'ballpoint',
        'corkscrew', 'bottlecap', 'pillow', 'quilt',
        'digital_clock', 'analog_clock', 'stopwatch',
        'lighter', 'ashcan', 'safe', 'cassette', 'disk', 'hard_disc',
        'space_bar', 'typewriter', 'abacus', 'modem', 'pinwheel',
        'rubber_eraser', 'pencil', 'fountain_pen', 'logo', 'signboard',
        'traffic_light', 'street_sign', 'doormat', 'plate_rack',
        'slot', 'vending', 'cash_machine', 'stretcher', 'crate',
        'carton', 'chest', 'desk', 'table_lamp', 'studio_couch',
        'mask', 'sock', 'shoe', 'sandal', 'running_shoe',
        'cloak', 'jersey', 'sweatshirt', 'suit', 'bow_tie',
        'book_jacket', 'puck', 'bathing_cap', 'ping-pong_ball',
        'wall_clock', 'window_shade',
    )

    # Soft reject
    SOFT_NON_PLANT_KEYWORDS = (
        'mushroom', 'agaric', 'gyromitra', 'bolete', 'earthstar',
        'hen-of-the-woods', 'coral_fungus', 'stinkhorn',
    )
    
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
            cls._class_names = sorted(
                d for d in os.listdir(data_path)
                if os.path.isdir(os.path.join(data_path, d))
            )
            cls._validation_model = MobileNetV2(weights='imagenet', include_top=True)
            print(f"Disease model loaded successfully with {len(cls._class_names)} classes")
        except Exception as e:
            print(f"Error loading models: {e}")
            cls._model = None
            cls._validation_model = None
            cls._class_names = []

    @classmethod
    def _looks_like_leaf_photo(cls, pil_img):
        small = pil_img.resize((128, 128))
        arr = np.asarray(small).astype(np.float32)
        if arr.ndim != 3 or arr.shape[2] < 3:
            return False

        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        if float(np.std(gray)) < 10.0:
            return False

        # Green check
        real_green = (g > r * 1.02) & (g > b * 1.02) & (g > 35) & ((g - np.maximum(r, b)) > 3)
        green_ratio = float(np.mean(real_green))
        if green_ratio < 0.10:
            return False

        # White bg
        white = (r > 225) & (g > 225) & (b > 225)
        white_ratio = float(np.mean(white))
        if white_ratio > 0.40 and green_ratio < 0.20:
            return False

        return True

    @classmethod
    def _name_hits(cls, name, keywords):
        name_l = name.lower().replace('-', '_').replace(' ', '_')
        tokens = set(name_l.split('_'))
        for keyword in keywords:
            kw = keyword.lower().replace('-', '_').replace(' ', '_')
            if len(kw) <= 3:
                if kw in tokens:
                    return True
            elif kw in name_l:
                return True
        return False

    @classmethod
    def is_plant_image(cls, img_path):
        if cls._validation_model is None:
            return False, 0.0, "validator_unavailable"

        try:
            img = Image.open(img_path).convert('RGB')
            img_resized = img.resize((224, 224))
            img_array = image.img_to_array(img_resized)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            preds = cls._validation_model.predict(img_array, verbose=0)
            decoded = decode_predictions(preds, top=5)[0]

            top_class = decoded[0][1]
            top_confidence = float(decoded[0][2])
            top_confidence_pct = top_confidence * 100
            looks_leafy = cls._looks_like_leaf_photo(img)

            print(
                "Plant gate:",
                [(name, round(float(conf) * 100, 1)) for _, name, conf in decoded],
                "leafy=", looks_leafy,
            )

            # Animal reject
            for _, class_name, confidence in decoded:
                if cls._name_hits(class_name.lower(), cls.ANIMAL_KEYWORDS) and float(confidence) >= 0.08:
                    return False, float(confidence) * 100, class_name

            # Object reject
            for _, class_name, confidence in decoded[:3]:
                if cls._name_hits(class_name.lower(), cls.HARD_NON_PLANT_KEYWORDS) and float(confidence) >= 0.12:
                    return False, float(confidence) * 100, class_name

            # Soft reject
            for _, class_name, confidence in decoded[:3]:
                if cls._name_hits(class_name.lower(), cls.SOFT_NON_PLANT_KEYWORDS) and float(confidence) >= 0.12:
                    if not looks_leafy:
                        return False, float(confidence) * 100, class_name

            leaf_score = 0.0
            best_leaf = None
            for _, class_name, confidence in decoded:
                conf = float(confidence)
                if cls._name_hits(class_name.lower(), cls.LEAF_KEYWORDS):
                    leaf_score += conf
                    if best_leaf is None or conf > best_leaf[1]:
                        best_leaf = (class_name, conf)

            # Plant accept
            if best_leaf and leaf_score >= 0.08 and looks_leafy:
                return True, best_leaf[1] * 100, best_leaf[0]

            # Green fallback
            if looks_leafy:
                return True, top_confidence_pct, "accepted_leaf_candidate"

            return False, top_confidence_pct, top_class

        except Exception as e:
            print(f"Image validation error: {e}")
            return False, 0.0, "validation_error"
    
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
            
            # Format name
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
        name = name.replace('_', ' ')
        name = name.replace('  ', ' - ')
        words = name.split()
        formatted_words = []
        
        for word in words:
            if word.isupper() and len(word) <= 3:
                formatted_words.append(word)
            else:
                formatted_words.append(word.capitalize())
        
        return ' '.join(formatted_words)
    
    @classmethod
    def is_loaded(cls):
        return cls._model is not None and cls._validation_model is not None
