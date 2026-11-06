import os
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from sklearn.metrics import confusion_matrix, classification_report

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'model', 'leaf_disease_model.h5')
    data_dir = os.path.join(base_dir, 'plant_disease_data', 'PlantVillage')
    
    # 1. Load model and class names
    print("Loading CNN model (this may take a few seconds)...")
    try:
        model = load_model(model_path)
        class_names = sorted(os.listdir(data_dir))
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Clean class names for display
    display_names = [name.replace('_', ' ').replace('  ', ' - ').title() for name in class_names]

    print("Gathering samples...")
    y_true = []
    y_pred = []
    
    # We will evaluate up to 15 random images per category to keep it fast (~225 images total)
    images_per_class = 15 
    
    for class_idx, class_name in enumerate(class_names):
        class_path = os.path.join(data_dir, class_name)
        if not os.path.isdir(class_path):
            continue
            
        images = [os.path.join(class_path, img) for img in os.listdir(class_path)
                  if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not images:
            continue
            
        # Sample images
        sample_size = min(images_per_class, len(images))
        sampled_images = random.sample(images, sample_size)
        
        print(f"Processing class '{class_name}' ({sample_size} images)...")
        
        for img_path in sampled_images:
            try:
                # Load and preprocess
                img = image.load_img(img_path, target_size=(256, 256))
                img_array = image.img_to_array(img)
                img_array = img_array / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                # Predict
                preds = model.predict(img_array, verbose=0)
                pred_idx = np.argmax(preds[0])
                
                y_true.append(class_idx)
                y_pred.append(pred_idx)
            except Exception as e:
                print(f"Error reading image {img_path}: {e}")

    # 2. Compute Confusion Matrix
    print("\nComputing confusion matrix...")
    cm = confusion_matrix(y_true, y_pred, labels=range(len(class_names)))
    
    # 3. Plot and save
    plt.figure(figsize=(14, 12))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='YlGnBu', 
        xticklabels=display_names, 
        yticklabels=display_names,
        cbar=True,
        square=True
    )
    
    plt.title("CNN Plant Leaf Disease Confusion Matrix", fontsize=16, fontweight='bold', pad=20)
    plt.ylabel("Actual Label", fontsize=12, fontweight='bold')
    plt.xlabel("Predicted Label", fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    
    # Save the confusion matrix plot
    output_path = os.path.join(base_dir, "leaf_disease_confusion_matrix.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"\nSuccess! Leaf Disease Confusion Matrix saved to: {output_path}")

if __name__ == '__main__':
    main()
