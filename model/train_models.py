import os
import csv
import numpy as np
import joblib
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train():
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'crop_data', 'Crop_recommendation.csv')
    model_dir = os.path.join(base_dir, 'model')
    
    os.makedirs(model_dir, exist_ok=True)
    
    # Load dataset using standard CSV library
    X = []
    y = []
    with open(csv_path, mode='r') as f:
        reader = csv.reader(f)
        header = next(reader) # skip header
        for row in reader:
            if not row:
                continue
            X.append([float(val) for val in row[:-1]])
            y.append(row[-1])
            
    X = np.array(X)
    y = np.array(y)
    
    print(f"Loaded {len(X)} rows of crop data.")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Split data into training set ({len(X_train)} samples) and test set ({len(X_test)} samples).")
    
    print("\n--- Model Evaluation ---")
    
    # 1. Evaluate Random Forest
    rf_eval = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_eval.fit(X_train, y_train)
    rf_pred = rf_eval.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_pred)
    print(f"Random Forest Classifier Accuracy Score: {rf_acc * 100:.2f}%")
    
    # 2. Evaluate SVM
    svm_eval = make_pipeline(
        StandardScaler(),
        SVC(probability=True, random_state=42)
    )
    svm_eval.fit(X_train, y_train)
    svm_pred = svm_eval.predict(X_test)
    svm_acc = accuracy_score(y_test, svm_pred)
    print(f"Support Vector Machine (SVM) Accuracy Score: {svm_acc * 100:.2f}%")

    # 3. Evaluate Gradient Boosting
    gb_eval = GradientBoostingClassifier(random_state=42)
    gb_eval.fit(X_train, y_train)
    gb_pred = gb_eval.predict(X_test)
    gb_acc = accuracy_score(y_test, gb_pred)
    print(f"Gradient Boosting Accuracy Score: {gb_acc * 100:.2f}%")
    print("------------------------\n")
    
    print("Training final models on the complete dataset...")
    
    # Final Random Forest (Save as crop_model.pkl for backward compatibility)
    final_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    final_rf.fit(X, y)
    rf_path = os.path.join(model_dir, 'crop_model.pkl')
    joblib.dump(final_rf, rf_path)
    print(f"Saved Random Forest model to {rf_path}")
    
    # Final SVM (Save as crop_svm_model.pkl)
    final_svm = make_pipeline(
        StandardScaler(),
        SVC(probability=True, random_state=42)
    )
    final_svm.fit(X, y)
    svm_path = os.path.join(model_dir, 'crop_svm_model.pkl')
    joblib.dump(final_svm, svm_path)
    print(f"Saved SVM model to {svm_path}")

    # Final Gradient Boosting (Save as crop_gb_model.pkl)
    final_gb = GradientBoostingClassifier(random_state=42)
    final_gb.fit(X, y)
    gb_path = os.path.join(model_dir, 'crop_gb_model.pkl')
    joblib.dump(final_gb, gb_path)
    print(f"Saved Gradient Boosting model to {gb_path}")
    
    print("\nTraining complete! All crop models are successfully compiled with final weights.")

if __name__ == '__main__':
    train()
