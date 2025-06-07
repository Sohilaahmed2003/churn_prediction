import pandas as pd
import streamlit as st
import joblib

@st.cache_data()
def load_data():
    try:
        df = pd.read_csv(r"c:\Users\sohila\OneDrive\csv\WA_Fn-UseC_-Telco-Customer-Churn.csv")  # Update with your dataset path
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load the dataset
df = load_data()

# Check if data loaded correctly
if df is not None:
    # Loading the model
    try:
        model = joblib.load(r"c:\Users\sohila\OneDrive\csv\charges_model.joblib")  # Update with your model path
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

    # --- Styling the page ---
    st.markdown("""
        <style>
            body {
                background-color: #F4F6F7;
            }
            h1 {
                font-size: 40px;
                color: #2E86C1;
                text-align: center;
                margin-bottom: 20px;
            }
            h2 {
                font-size: 24px;
                color: #2874A6;
            }
            .stButton>button {
                background-color: #3498DB;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 18px;
            }
            .stButton>button:hover {
                background-color: #5DADE2;
            }
            .prediction-box {
                background-color: #D6EAF8;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 28px;
                font-weight: bold;
                color: #1A5276;
                margin-top: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Streamlit Interface ---
    st.title("📊 Customer Churn Prediction")
    st.subheader("Fill in customer details:")

    # --- Function to capture user inputs ---
    def user_input_features():
        col1, col2 = st.columns(2)

        with col1:
            tenure = st.slider("Tenure (Months)", min_value=0, max_value=72, value=12)
            monthly_charges = st.slider("Monthly Charges ($)", min_value=0, max_value=200, value=50)
            total_charges = st.slider("Total Charges ($)", min_value=0.0, max_value=10000.0, value=100.0)

        with col2:
            gender = st.selectbox("Gender", df['gender'].unique())
            partner = st.selectbox("Partner", df['Partner'].unique())
            dependents = st.selectbox("Dependents", df['Dependents'].unique())

        # Create input DataFrame
        data = {
            "tenure": tenure,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
            "gender": gender,
            "Partner": partner,
            "Dependents": dependents
        }
        features = pd.DataFrame(data, index=[0])
        return features

    # --- Capture User Input ---
    user_input = user_input_features()

    # --- Predict and Display ---
    if st.button("🔮 Predict Churn"):
        try:
            prediction = model.predict(user_input)[0]
            prediction_label = "Churn" if prediction == 1 else "No Churn"
            st.markdown(f"""
                <div class="prediction-box">
                    🏷️ Prediction: <br> <span style='color:#154360;'>{prediction_label}</span>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error during prediction: {e}")
else:
    st.error("Failed to load data. Please check your CSV file path or content.")
