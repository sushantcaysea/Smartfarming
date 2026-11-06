import os
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def evaluate_live_accuracy(sample_size=50, seed=2):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        tf.random.set_seed(seed)
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'model', 'leaf_disease_model.h5')
    data_dir = os.path.join(base_dir, 'plant_disease_data', 'PlantVillage')
    
    # 1. Load model and class names
    print("Loading Leaf Disease CNN Model (this may take a few seconds)...")
    try:
        model = load_model(model_path)
        class_names = sorted(os.listdir(data_dir))
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    print("Gathering image paths...")
    all_images = []
    for category in class_names:
        category_path = os.path.join(data_dir, category)
        if os.path.isdir(category_path):
            images = [os.path.join(category_path, img) for img in os.listdir(category_path) 
                      if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
            # Store tuple of (image_path, true_label_index, true_label_name)
            true_idx = class_names.index(category)
            for img in images:
                all_images.append((img, true_idx, category))
                
    if not all_images:
        print("No images found in plant_disease_data/PlantVillage.")
        return
        
    # 2. Select a random sample to run quickly
    sample_size = min(sample_size, len(all_images))
    sampled_data = random.sample(all_images, sample_size)
    
    print(f"\nEvaluating {sample_size} random images from the dataset...")
    print("-" * 70)
    
    correct_count = 0
    
    for idx, (img_path, true_idx, true_name) in enumerate(sampled_data):
        try:
            # Preprocess image for the CNN (resize to 256x256 and scale to 0-1)
            img = image.load_img(img_path, target_size=(256, 256))
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Predict
            preds = model.predict(img_array, verbose=0)
            pred_idx = np.argmax(preds[0])
            pred_name = class_names[pred_idx]
            confidence = np.max(preds[0]) * 100
            
            is_correct = (pred_idx == true_idx)
            status = "CORRECT" if is_correct else "INCORRECT"
            if is_correct:
                correct_count += 1
                
            print(f"[{idx+1:02d}/{sample_size}] True: {true_name:<30} | Pred: {pred_name:<30} | Conf: {confidence:.2f}% | {status}")
            
        except Exception as e:
            print(f"Error processing image {img_path}: {e}")
            
    # 3. Print Final Accuracy Report
    accuracy = (correct_count / sample_size) * 100
    print("-" * 70)
    print("                      EVALUATION RESULTS                      ")
    print("-" * 70)
    print(f"Total Evaluated Images:  {sample_size}")
    print(f"Correct Predictions:     {correct_count}")
    print(f"Incorrect Predictions:   {sample_size - correct_count}")
    print(f"Overall Model Accuracy:  {accuracy:.2f}%")
    print("-" * 70)

if __name__ == '__main__':
    # You can change the sample size here (e.g., set to 50 for a quick 10-second demo)
    evaluate_live_accuracy(sample_size=50)
