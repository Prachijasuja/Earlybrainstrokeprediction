from flask import Flask, render_template, request
import joblib
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model and scaler
#model = joblib.load('stroke_prediction_model.pkl')
#scaler = joblib.load('scaler.pkl')

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to predict stroke
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Collect input values from the form
        gender = request.form['gender']
        age = float(request.form['age'])
        hypertension = int(request.form['hypertension'])
        heart_disease = int(request.form['heart_disease'])
        ever_married = request.form['ever_married']
        work_type = request.form['work_type']
        residence_type = request.form['residence_type']
        avg_glucose_level = float(request.form['avg_glucose_level'])
        bmi = float(request.form['bmi'])
        
        # Additional features (make sure these are consistent with training data)
        smoking_status = request.form['smoking_status']  # Assuming this feature exists in your model
        
        # Convert categorical features to numeric (one-hot encoding or label encoding)
        gender = 1 if gender == 'Male' else 0
        ever_married = 1 if ever_married == 'Yes' else 0
        work_type = {'Private': 0, 'Self-employed': 1, 'Govt_job': 2, 'children': 3, 'Never_worked': 4}.get(work_type, -1)
        residence_type = 1 if residence_type == 'Urban' else 0
        smoking_status = {'never smoked': 0, 'smokes': 1, 'formerly smoked': 2}.get(smoking_status, -1)

        # Ensure you are passing 21 features (e.g., by adding missing ones like 'smoking_status')
        # You may need to add other features here based on what was used during training
        features = np.array([gender, age, hypertension, heart_disease, ever_married, work_type, residence_type,
                             avg_glucose_level, bmi, smoking_status]).reshape(1, -1)

        # Scale the features using the loaded scaler
        scaled_features = scaler.transform(features)

        # Make prediction
        prediction = model.predict(scaled_features)

        # Display the result
        stroke_chance = 'Yes' if prediction[0] == 1 else 'No'
        return render_template('index.html', prediction_text=f"Prediction: {stroke_chance} (Stroke Likelihood)")

if __name__ == '__main__':
    app.run(debug=True)
