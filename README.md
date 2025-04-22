
# NourishKidsAgri: AI-powered Agricultural Assistant 🌱

NourishKidsAgri is an AI-driven platform designed to assist farmers in making informed decisions for efficient and sustainable farming. By leveraging machine learning and advanced algorithms, the platform offers crop recommendations, irrigation management, and an AI-powered chatbot for instant farming insights.

### Key Features:
- **Crop Recommendations**: Personalized crop suggestions based on local weather, soil, and environmental data.
- **Irrigation Management**: Tailored irrigation advice to ensure optimal water usage and crop health.
- **AI Chatbot**: Get instant answers to your farming-related questions and optimize your farm's potential.

---

## How It Works:

### Crop Recommendation System 🌾:
The system uses a machine learning model trained on a large dataset to provide the best crop suggestions for your farm's conditions. The model considers:
- Soil composition (N, P, K, pH)
- Environmental factors (temperature, humidity, rainfall)

### Irrigation Management 💧:
The platform also provides smart irrigation recommendations, optimizing water usage for your specific crop and farm setup.

### AI Chatbot 💬:
Interact with the AI chatbot to ask farming-related questions. The chatbot gives you instant, actionable insights.

---

## Key Technologies Used:
- **Streamlit** – Frontend & UI framework.
- **scikit-learn** – For machine learning and predictive modeling.
- **scikit-fuzzy** – To implement fuzzy logic for irrigation management.
- **XGBoost** – For gradient boosting in crop prediction models.
- **NetworkX** – Dependency required by fuzzy logic module.
- **Pandas, NumPy, Pillow** – For data handling and image support.

---

## Training the Crop Recommendation Model

To train the crop recommendation model, we used the following libraries:

### Basic Libraries:
- **NumPy**: For numerical computations
- **Pandas**: For working with datasets (dataframes)
- **os**: For handling file paths
- **kagglehub**: For downloading datasets from Kaggle

### Data Visualization:
- **Matplotlib**: For basic plotting
- **Seaborn**: For attractive and informative statistical graphics

### Machine Learning Models:
- **Logistic Regression**: A linear model used as a baseline classifier
- **RandomForestClassifier**: A robust ensemble learning model for classification
- **XGBClassifier**: An efficient gradient boosting model from XGBoost

### Preprocessing and Splitting Data:
- **train_test_split**: To split data into training and test sets
- **StandardScaler**: To normalize or scale features
- **LabelEncoder**: To encode categorical labels as numerical values

### Hyperparameter Tuning:
- **GridSearchCV**: For automatic hyperparameter tuning to find the best model parameters

### Model Evaluation:
- **accuracy_score**: For measuring the model's accuracy
- **confusion_matrix**: For visualizing prediction results
- **classification_report**: For detailed metrics such as precision, recall, F1-score
- **learning_curve**: For evaluating the model's learning behavior

### For Saving the Model:
- **joblib**: To save and load the trained model

---

## File Structure:

Here’s an overview of the main files in the project:

```
agriculture.db            # Database storing agricultural data
amain.py                  # Main Python script (entry point)
app.py                    # Streamlit app for the user interface
chatbot.py                # Chatbot functionality
Crop_recommendation.csv   # Data for crop recommendations
database.py               # Database management functions
farming_data.db           # Database for farming-related data
irrigation.py             # Irrigation recommendation logic
label_encoder.pkl         # Pre-trained label encoder for predictions
Procfile                  # File for deployment instructions (e.g., on Heroku)
requirements.txt          # Dependencies for the project
xgb_crop_model.pkl        # Pre-trained XGBoost model for crop recommendations
__pycache__               # Compiled Python files
```

---

## How to Run Locally:

1. Clone the repository or download the project files.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    streamlit run app.py
    ```
4. Open your browser and visit [localhost:8501](http://localhost:8501) to access the app.

---

## Deployment:

You can deploy the app on platforms like [Streamlit Cloud](https://streamlit.io/cloud) or [Heroku](https://www.heroku.com/). Make sure to include the `Procfile` for Heroku deployment.

---

## Contribution:

Feel free to fork the project, create pull requests, and improve features or fix bugs. Contributions are welcome!

---
