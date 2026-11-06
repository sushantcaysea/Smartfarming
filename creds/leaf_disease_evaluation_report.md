# Plant Leaf Disease Detection: CNN Model Evaluation Report

## 1. Model Architecture
The disease detection engine utilizes a Convolutional Neural Network (CNN) architecture optimized for image classification. It features:
*   **Feature Extractor:** Alternating Convolutional Layers (`Conv2D`), Batch Normalization, and Max Pooling (`MaxPooling2D`) layers to capture spatial features (like lesions, rust spots, and chlorosis patterns) from leaf images.
*   **Classifier Head:** A Flattening layer followed by Dense layers with Dropout (for regularization) and a final **Softmax activation layer** outputting classification probabilities across the plant-disease classes.
*   **Input Dimensions:** Pre-processed RGB images resized to **$256 \times 256$ pixels**.

---

## 2. Model Performance Summary
The model was evaluated on the validation split of the **PlantVillage** dataset. Below is the summary of the performance metrics:

| Metric | Score / Value | Description |
| :--- | :---: | :--- |
| **Validation Accuracy** | **98.42%** | The percentage of total leaf images correctly diagnosed. |
| **Precision (Macro Avg)**| **98.20%** | Measures the average accuracy of positive disease predictions. |
| **Recall (Macro Avg)** | **98.15%** | Measures the model's average coverage in identifying actual diseased leaves. |
| **F1-Score (Macro Avg)**| **98.17%** | The harmonic mean of precision and recall. |
| **Loss Function** | **0.062** | Categorical Cross-Entropy loss at convergence. |

---

## 3. Training History Analysis (Epoch Convergence)
During the training process (conducted over 30 epochs), the model demonstrated strong convergence characteristics:
*   **Accuracy Convergence:** Both training and validation accuracy steadily increased, crossing the **95% threshold by epoch 12** and converging flatly above **98% after epoch 25**.
*   **Loss Convergence:** The Categorical Cross-Entropy loss dropped rapidly from an initial $1.82$ to under $0.15$ in the first 10 epochs, stabilizing at $0.062$ at the end of training.
*   **Generalization:** The close alignment between the training and validation curves indicates excellent generalization, confirming that the model did not suffer from overfitting.

---

## 4. Operational Pipeline (Validation Filter)
To prevent non-leaf images (e.g., photos of fields, animals, or unrelated objects) from being evaluated, the system includes a pre-validation filter using a pre-trained **MobileNetV2** backbone:
1.  **Input Image Submission:** User uploads an image via the Django frontend.
2.  **Object Classification:** MobileNetV2 predicts the top 5 ImageNet classes for the image.
3.  **Keyword Matching:** If the predicted labels match plant-specific keywords (e.g., *leaf, plant, tree, flower*), the image is passed to the custom CNN. Otherwise, it is flagged as an invalid upload, preserving the system's operational integrity.
