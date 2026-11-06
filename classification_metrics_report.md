# Classification Performance Evaluation Report

This report documents Accuracy, Precision, Recall, and F1-Score for **Random Forest**, **SVM**, and **Gradient Boosting** on the validation test set (440 samples).

---

## 1. Global Performance Overview

| Model | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest** | **99.32%** | **99.37%** | **99.32%** | **99.32%** |
| **Support Vector Machine (SVM)** | **96.82%** | **97.15%** | **96.82%** | **96.80%** |
| **Gradient Boosting** | **98.18%** | **98.43%** | **98.18%** | **98.19%** |

---

## 2. Per-Class Performance: Random Forest

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

---

## 3. Per-Class Performance: Support Vector Machine (SVM)

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

## 4. Per-Class Performance: Gradient Boosting

| Crop Class | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
| Apple | 100.00% | 100.00% | 100.00% |
| Banana | 100.00% | 100.00% | 100.00% |
| Blackgram | 95.24% | 100.00% | 97.56% |
| Chickpea | 100.00% | 100.00% | 100.00% |
| Coconut | 100.00% | 96.30% | 98.11% |
| Coffee | 100.00% | 100.00% | 100.00% |
| Cotton | 94.44% | 100.00% | 97.14% |
| Grapes | 100.00% | 100.00% | 100.00% |
| Jute | 82.14% | 100.00% | 90.20% |
| Kidneybeans | 100.00% | 100.00% | 100.00% |
| Lentil | 91.67% | 100.00% | 95.65% |
| Maize | 100.00% | 95.24% | 97.56% |
| Mango | 100.00% | 100.00% | 100.00% |
| Mothbeans | 100.00% | 95.83% | 97.87% |
| Mungbean | 100.00% | 100.00% | 100.00% |
| Muskmelon | 100.00% | 100.00% | 100.00% |
| Orange | 100.00% | 100.00% | 100.00% |
| Papaya | 100.00% | 100.00% | 100.00% |
| Pigeonpeas | 100.00% | 95.65% | 97.78% |
| Pomegranate | 100.00% | 100.00% | 100.00% |
| Rice | 100.00% | 78.95% | 88.24% |
| Watermelon | 100.00% | 100.00% | 100.00% |

---

## 5. Conclusion
1. Random Forest leads overall accuracy at **99.32%**.
2. Gradient Boosting is close behind at **98.18%**.
3. SVM remains competitive at **96.82%**.
