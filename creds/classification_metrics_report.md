# Classification Performance Evaluation Report

This report documents the detailed classification metrics (Accuracy, Precision, Recall, and F1-Score) for the **Random Forest** and **Support Vector Machine (SVM)** models on the validation test set (440 samples).

---

## 1. Global Performance Overview

| Model | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest** | **99.32%** | **99.37%** | **99.32%** | **99.32%** |
| **Support Vector Machine (SVM)** | **96.82%** | **97.15%** | **96.82%** | **96.80%** |

---

## 2. Per-Class Performance: Random Forest (Selected Model)

Below is the detailed classification report for each crop class under the **Random Forest** model:

| Crop Class | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
| Apple | 100.00% | 100.00% | 100.00% |
| Banana | 100.00% | 100.00% | 100.00% |
| Blackgram | 100.00% | 100.00% | 100.00% |
| Chickpea | 100.00% | 100.00% | 100.00% |
| Coconut | 100.00% | 100.00% | 100.00% |
| Coffee | 100.00% | 100.00% | 100.00% |
| Cotton | 100.00% | 100.00% | 100.00% |
| Grapes | 100.00% | 100.00% | 100.00% |
| Jute | 92.00% | 100.00% | 95.83% |
| Kidneybeans | 100.00% | 100.00% | 100.00% |
| Lentil | 91.67% | 100.00% | 95.65% |
| Maize | 100.00% | 100.00% | 100.00% |
| Mango | 100.00% | 100.00% | 100.00% |
| Mothbeans | 100.00% | 95.83% | 97.87% |
| Mungbean | 100.00% | 100.00% | 100.00% |
| Muskmelon | 100.00% | 100.00% | 100.00% |
| Orange | 100.00% | 100.00% | 100.00% |
| Papaya | 100.00% | 100.00% | 100.00% |
| Pigeonpeas | 100.00% | 100.00% | 100.00% |
| Pomegranate | 100.00% | 100.00% | 100.00% |
| Rice | 100.00% | 89.47% | 94.44% |
| Watermelon | 100.00% | 100.00% | 100.00% |

* **Precision:** The percentage of predicted crop instances that were correct.
* **Recall:** The percentage of actual crop instances that the model correctly identified.
* **F1-Score:** The harmonic mean of Precision and Recall.

---

## 3. Per-Class Performance: Support Vector Machine (SVM)

Below is the detailed classification report for each crop class under the **Support Vector Machine (SVM)** model:

| Crop Class | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
| Apple | 100.00% | 100.00% | 100.00% |
| Banana | 100.00% | 100.00% | 100.00% |
| Blackgram | 100.00% | 95.00% | 97.44% |
| Chickpea | 100.00% | 100.00% | 100.00% |
| Coconut | 100.00% | 100.00% | 100.00% |
| Coffee | 94.44% | 100.00% | 97.14% |
| Cotton | 94.44% | 100.00% | 97.14% |
| Grapes | 100.00% | 100.00% | 100.00% |
| Jute | 77.78% | 91.30% | 84.00% |
| Kidneybeans | 90.91% | 100.00% | 95.24% |
| Lentil | 78.57% | 100.00% | 88.00% |
| Maize | 100.00% | 95.24% | 97.56% |
| Mango | 100.00% | 100.00% | 100.00% |
| Mothbeans | 100.00% | 91.67% | 95.65% |
| Mungbean | 100.00% | 100.00% | 100.00% |
| Muskmelon | 100.00% | 100.00% | 100.00% |
| Orange | 100.00% | 100.00% | 100.00% |
| Papaya | 100.00% | 100.00% | 100.00% |
| Pigeonpeas | 100.00% | 91.30% | 95.45% |
| Pomegranate | 100.00% | 100.00% | 100.00% |
| Rice | 92.86% | 68.42% | 78.79% |
| Watermelon | 100.00% | 100.00% | 100.00% |

---

## 4. Conclusion & Key Takeaways
1. **Precision / Recall Stability:** The Random Forest Classifier maintains virtually 100% Precision and Recall across almost all classes, whereas the SVM shows slight drops in certain crop categories.
2. **Tabular Robustness:** Since the dataset consists of soil parameters and weather conditions with clear boundary thresholds, Random Forest dominates with **99.32%** overall accuracy.
