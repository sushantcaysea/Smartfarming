# Crop Recommendation Model Comparison Report

This report evaluates and compares the performance of two machine learning models—**Random Forest Classifier** and **Support Vector Machine (SVM)**—implemented in the Smart Farming decision support system for predicting crop suitability based on soil chemistry and meteorological conditions.

---

## 1. Executive Performance Summary

A split-validation test was conducted using $80\%$ of the historical dataset for training and $20\%$ for validation. The results are as follows:

| Metric | Random Forest Classifier | Support Vector Machine (SVM) |
| :--- | :---: | :---: |
| **Validation Accuracy** | **99.32%** | **96.82%** |
| **Feature Scaling Required** | No | Yes (Standardization) |
| **Outlier Robustness** | Excellent | Moderate |
| **Prediction Probability Basis** | Frequency of Decision Trees | Platt Scaling (Sigmoid function) |
| **Decision Boundary** | Orthogonal Axis-Aligned Splitting | Smooth Maximum-Margin Hyperplane |
| **Production Recommendation** | **Selected (Primary)** | Decommissioned / Reference Only |

---

## 2. Algorithmic Profiles & Mathematical Formulations

### 2.1. Random Forest Classifier (Selected Model)
The Random Forest Classifier is an ensemble learning method that constructs a forest of $100$ independent decision trees using bootstrap aggregation (bagging) and random feature selection.

#### Mathematical Split Criterion (Gini Impurity)
At each node, the optimal split is calculated by maximizing the **Gini Gain** (reduction in Gini Impurity). The Gini Impurity $I_G(t)$ for a node $t$ containing $C = 22$ crop classes is defined as:
$$I_G(t) = 1 - \sum_{i=1}^{C} p_i^2$$
Where $p_i$ is the probability/proportion of samples belonging to crop class $i$ in node $t$.

#### Probability Recommendation Score
The final suitability match score for crop class $c$ is computed directly as the fraction of trees ($B = 100$) that classify input vector $x$ as crop $c$:
$$P(y = c \mid x) = \frac{1}{B} \sum_{b=1}^{B} I(T_b(x) = c)$$
Where:
* $T_b(x)$ is the prediction of the $b$-th decision tree.
* $I(\cdot)$ is the indicator function ($1$ if the tree predicts class $c$, $0$ otherwise).

---

### 2.2. Support Vector Machine (SVM) Classifier
The SVM classifier maps inputs to a high-dimensional feature space and constructs an optimal decision boundary (hyperplane) that maximizes the separation margin between classes.

#### Non-Linear Kernel Projection (RBF Kernel)
To handle non-linear crop thresholds, the model projects the input feature vector $x$ using a **Radial Basis Function (RBF) Kernel**:
$$K(x_k, x) = \exp\left( -\gamma \|x_k - x\|^2 \right)$$
Where $x_k$ is a support vector and $\gamma$ is the kernel scale parameter.

#### Multi-Class Strategy (One-vs-One)
For $K = 22$ crop categories, SVM trains a total of $L = \frac{K(K-1)}{2} = 231$ binary classifiers. The final classification decision is determined by a majority vote across all $231$ classifiers:
$$\hat{y} = \arg\max_{c \in \{1, \dots, K\}} \sum_{i < j} I\left( \text{sign}\left(f_{i,j}(x)\right) == c \right)$$

#### Probability Mapping (Platt Scaling)
Because SVM is a non-probabilistic margin classifier, obtaining suitability scores requires **Platt Scaling**, which fits an additional sigmoid calibration model over the decision scores:
$$P(y = c \mid x) = \frac{1}{1 + \exp(A \cdot f(x) + B)}$$
Where $A$ and $B$ are parameters learned via internal cross-validation.

---

## 3. Comparative Analysis: Why Random Forest Outperforms SVM

### 3.1. Nature of Agricultural Data
Agricultural datasets (soil nutrient boundaries, rainfall levels, pH ranges) are governed by strict physical thresholds. For example, a specific crop might thrive in a pH range of $6.0$ to $7.0$, but wither completely at pH $5.8$. 
* **Random Forest** naturally captures these step-function conditions via rectangular axis-aligned splits.
* **SVM** attempts to fit smooth continuous hyperplanes, which tends to smear these strict thresholds, leading to lower classification resolution near boundary conditions.

### 3.2. Probability Calibration Behavior
* **Random Forest** confidence percentages reflect the consensus of multiple decision trees. This is highly reliable for ranking top recommendations (e.g., showing top 5 crop recommendations).
* **SVM** probability estimates are warped by Platt scaling, sometimes producing high-confidence matches for classes that are far from the center of the training clusters, or introducing scaling artifacts.

### 3.3. Preprocessing Sensitivity
* **SVM** is highly sensitive to the scale of input features and requires a standard scaler pipeline (`StandardScaler()`). An unscaled input dramatically reduces SVM's accuracy.
* **Random Forest** is scale-invariant and robust to variations in input magnitudes, making it more resilient to noisy or unnormalized inputs.

---

## 4. Final Recommendation

Based on the evaluation metrics, **Random Forest is designated as the sole recommendation engine** in the Smart Farming application due to its:
1. Higher validation accuracy (**99.32%** vs **96.82%**).
2. Natural ability to model threshold-based environmental parameters.
3. Stable and directly interpretable vote-based suitability percentages.
