import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix


def generate_report():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'crop_data', 'Crop_recommendation.csv')
    report_path = os.path.join(base_dir, 'classification_metrics_report.md')

    X = []
    y = []
    with open(csv_path, mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if not row:
                continue
            X.append([float(val) for val in row[:-1]])
            y.append(row[-1])

    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    svm_model = make_pipeline(StandardScaler(), SVC(probability=True, random_state=42))
    svm_model.fit(X_train, y_train)

    gb_model = GradientBoostingClassifier(random_state=42)
    gb_model.fit(X_train, y_train)

    rf_pred = rf_model.predict(X_test)
    svm_pred = svm_model.predict(X_test)
    gb_pred = gb_model.predict(X_test)

    rf_acc = accuracy_score(y_test, rf_pred)
    svm_acc = accuracy_score(y_test, svm_pred)
    gb_acc = accuracy_score(y_test, gb_pred)

    rf_report = classification_report(y_test, rf_pred, output_dict=True, zero_division=0)
    svm_report = classification_report(y_test, svm_pred, output_dict=True, zero_division=0)
    gb_report = classification_report(y_test, gb_pred, output_dict=True, zero_division=0)

    def weighted(report, key):
        return report['weighted avg'][key] * 100

    # Clear terminal summary table
    print("\n" + "=" * 72)
    print("                 EVALUATION METRICS (TEST SET: 440 samples)")
    print("=" * 72)
    print(f"{'Metric':<12} {'Random Forest':>16} {'SVM':>16} {'Gradient Boosting':>18}")
    print("-" * 72)
    print(f"{'Accuracy':<12} {rf_acc * 100:>15.2f}% {svm_acc * 100:>15.2f}% {gb_acc * 100:>17.2f}%")
    print(f"{'Precision':<12} {weighted(rf_report, 'precision'):>15.2f}% {weighted(svm_report, 'precision'):>15.2f}% {weighted(gb_report, 'precision'):>17.2f}%")
    print(f"{'Recall':<12} {weighted(rf_report, 'recall'):>15.2f}% {weighted(svm_report, 'recall'):>15.2f}% {weighted(gb_report, 'recall'):>17.2f}%")
    print(f"{'F1-Score':<12} {weighted(rf_report, 'f1-score'):>15.2f}% {weighted(svm_report, 'f1-score'):>15.2f}% {weighted(gb_report, 'f1-score'):>17.2f}%")
    print("=" * 72)

    print("\nDecimal form (like report table):")
    print(f"{'Metric':<12} {'Random Forest':>16} {'SVM':>16} {'Gradient Boosting':>18}")
    print("-" * 72)
    print(f"{'Accuracy':<12} {rf_acc:>16.2f} {svm_acc:>16.2f} {gb_acc:>18.2f}")
    print(f"{'Precision':<12} {rf_report['weighted avg']['precision']:>16.2f} {svm_report['weighted avg']['precision']:>16.2f} {gb_report['weighted avg']['precision']:>18.2f}")
    print(f"{'Recall':<12} {rf_report['weighted avg']['recall']:>16.2f} {svm_report['weighted avg']['recall']:>16.2f} {gb_report['weighted avg']['recall']:>18.2f}")
    print(f"{'F1-Score':<12} {rf_report['weighted avg']['f1-score']:>16.2f} {svm_report['weighted avg']['f1-score']:>16.2f} {gb_report['weighted avg']['f1-score']:>18.2f}")
    print("=" * 72)

    def per_class_rows(report):
        rows = []
        for crop in sorted(set(y_test)):
            p = report[crop]['precision'] * 100
            r = report[crop]['recall'] * 100
            f = report[crop]['f1-score'] * 100
            rows.append(f"| {crop.capitalize()} | {p:.2f}% | {r:.2f}% | {f:.2f}% |")
        return "\n".join(rows)

    md_content = f"""# Classification Performance Evaluation Report

This report documents Accuracy, Precision, Recall, and F1-Score for **Random Forest**, **SVM**, and **Gradient Boosting** on the validation test set (440 samples).

---

## 1. Global Performance Overview

| Model | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest** | **{rf_acc * 100:.2f}%** | **{weighted(rf_report, 'precision'):.2f}%** | **{weighted(rf_report, 'recall'):.2f}%** | **{weighted(rf_report, 'f1-score'):.2f}%** |
| **Support Vector Machine (SVM)** | **{svm_acc * 100:.2f}%** | **{weighted(svm_report, 'precision'):.2f}%** | **{weighted(svm_report, 'recall'):.2f}%** | **{weighted(svm_report, 'f1-score'):.2f}%** |
| **Gradient Boosting** | **{gb_acc * 100:.2f}%** | **{weighted(gb_report, 'precision'):.2f}%** | **{weighted(gb_report, 'recall'):.2f}%** | **{weighted(gb_report, 'f1-score'):.2f}%** |

---

## 2. Per-Class Performance: Random Forest

| Crop Class | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
{per_class_rows(rf_report)}

---

## 3. Per-Class Performance: Support Vector Machine (SVM)

| Crop Class | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
{per_class_rows(svm_report)}

---

## 4. Per-Class Performance: Gradient Boosting

| Crop Class | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
{per_class_rows(gb_report)}

---

## 5. Conclusion
1. Random Forest leads overall accuracy at **{rf_acc * 100:.2f}%**.
2. Gradient Boosting is close behind at **{gb_acc * 100:.2f}%**.
3. SVM remains competitive at **{svm_acc * 100:.2f}%**.
"""

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"\nGenerated classification report: {report_path}")

    classes = sorted(list(set(y_test)))

    def save_cm(preds, title, cmap, filename):
        plt.figure(figsize=(14, 12))
        cm = confusion_matrix(y_test, preds, labels=classes)
        sns.heatmap(
            cm, annot=True, fmt='d', cmap=cmap,
            xticklabels=[c.capitalize() for c in classes],
            yticklabels=[c.capitalize() for c in classes],
        )
        plt.title(title, fontsize=16, pad=20)
        plt.ylabel('Actual Crop', fontsize=12)
        plt.xlabel('Predicted Crop', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        path = os.path.join(base_dir, filename)
        plt.savefig(path, dpi=300)
        plt.close()
        print(f"Saved confusion matrix: {path}")

    save_cm(rf_pred, 'Random Forest Crop Suitability Confusion Matrix', 'Greens', 'random_forest_confusion_matrix.png')
    save_cm(svm_pred, 'SVM Crop Suitability Confusion Matrix', 'Blues', 'svm_confusion_matrix.png')
    save_cm(gb_pred, 'Gradient Boosting Crop Suitability Confusion Matrix', 'Oranges', 'gradient_boosting_confusion_matrix.png')

    print("\n" + "-" * 72)
    print("RANDOM FOREST CLASSIFICATION REPORT")
    print("-" * 72)
    print(classification_report(y_test, rf_pred, zero_division=0))

    print("\n" + "-" * 72)
    print("SVM CLASSIFICATION REPORT")
    print("-" * 72)
    print(classification_report(y_test, svm_pred, zero_division=0))

    print("\n" + "-" * 72)
    print("GRADIENT BOOSTING CLASSIFICATION REPORT")
    print("-" * 72)
    print(classification_report(y_test, gb_pred, zero_division=0))


if __name__ == '__main__':
    generate_report()
