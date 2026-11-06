# Rainfall Prediction System — Algorithm Steps

These are the following steps used in the rainfall prediction system.
Algorithms used: Random Forest, SVM, and Gradient Boosting.


==================================================
1) RANDOM FOREST ALGORITHM
==================================================

The algorithm follows these steps:

1. Collect weather dataset and split into training and testing sets.
2. Create Random Forest model with multiple decision trees.
   a. Code: RandomForestClassifier(n_estimators=100, random_state=42)
3. Train each tree on random samples of weather data.
4. At each node, choose the best split using Gini impurity.
   a. Formula: I_G(t) = 1 - sum(p_i^2)
5. Save the trained Random Forest model.
6. Take user weather inputs in the web app.
7. Send input values to the Random Forest model.
8. Get class probabilities using predict_proba().
   a. Code: probabilities = model.predict_proba(input_data)[0]
   b. Formula: P(y=c|x) = (1/B) * sum(p_b(c|x))
9. Choose highest probability and convert to confidence.
   a. Code: index = np.argmax(probabilities)
   b. Code: confidence = round(100 * np.max(probabilities), 2)
   c. Formula: y_hat = argmax P(y=c|x)
   d. Formula: Confidence(%) = max(P(y=c|x)) * 100
10. Show rainfall prediction result and confidence on the webpage.


==================================================
2) SVM ALGORITHM
==================================================

The algorithm follows these steps:

1. Collect weather dataset and split into training and testing sets.
2. Scale weather features using StandardScaler.
   a. Code: make_pipeline(StandardScaler(), SVC(probability=True, random_state=42))
3. Train SVM using RBF kernel.
   a. Formula: K(x_k, x) = exp(-gamma * ||x_k - x||^2)
4. Build decision boundary to separate rainfall classes.
   a. Formula: f(x) = sum(alpha_k * y_k * K(x_k, x)) + b
5. Enable probability output using Platt scaling.
   a. Code: SVC(probability=True, random_state=42)
   b. Formula: P(y=c|x) = 1 / (1 + exp(A * f(x) + B))
6. Save the trained SVM model.
7. Take user weather inputs in the web app.
8. Scale input values and send them to the SVM model.
9. Get probabilities, choose highest class, and convert to confidence.
   a. Code: probabilities = model.predict_proba(input_data)[0]
   b. Code: confidence = round(100 * np.max(probabilities), 2)
   c. Formula: y_hat = argmax P(y=c|x)
   d. Formula: Confidence(%) = max(P(y=c|x)) * 100
10. Show rainfall prediction result and confidence on the webpage.


==================================================
3) GRADIENT BOOSTING ALGORITHM
==================================================

The algorithm follows these steps:

1. Collect weather dataset and split into training and testing sets.
2. Create Gradient Boosting model.
   a. Code: GradientBoostingClassifier(random_state=42)
3. Train the first tree on weather data.
4. Find prediction errors of the previous tree.
5. Train the next tree to correct those errors.
6. Repeat for many boosting stages and combine tree scores.
   a. Formula: F_M(x) = F_0(x) + learning_rate * sum(h_m(x))
7. Convert final scores into class probabilities using Softmax.
   a. Formula: P(y=c|x) = exp(F_c(x)) / sum(exp(F_j(x)))
8. Save the trained Gradient Boosting model.
9. Take user weather inputs, run predict_proba(), and convert to confidence.
   a. Code: probabilities = model.predict_proba(input_data)[0]
   b. Code: confidence = round(100 * np.max(probabilities), 2)
   c. Formula: y_hat = argmax P(y=c|x)
   d. Formula: Confidence(%) = max(P(y=c|x)) * 100
10. Show rainfall prediction result and confidence on the webpage.


==================================================
COMMON WEB APP FLOW
==================================================

The rainfall prediction web app follows these steps:

1. User opens rainfall prediction page.
2. User enters weather parameters.
3. System validates input values.
4. Run Random Forest model.
5. Run SVM model.
6. Run Gradient Boosting model.
7. Get prediction and confidence from each model.
8. Show final rainfall prediction results on the webpage.


==================================================
IMPORTANT NOTES
==================================================

1. These steps are for a rainfall prediction system.
2. They are not for leaf disease CNN.
3. If the project predicts Rain / No Rain, use Classifier models.
4. If the project predicts rainfall amount in mm, use Regressor models and MSE instead of Softmax/confidence %.
5. Confidence formula above is for classification:
   Confidence(%) = Probability * 100
