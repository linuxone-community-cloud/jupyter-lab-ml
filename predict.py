import streamlit as st
import pandas as pd
import numpy as np
import joblib
import base64
import warnings
from datetime import datetime
import plotly.express as px

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="⚖️ Court Case Priority Predictor",
    page_icon="⚖️",
    layout="wide"
)

# ============================
# 🎯 Load Model & Metadata
# ============================
@st.cache_resource
def load_artifacts():
    model = joblib.load("best_priority_model.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    feature_names = joblib.load("feature_names.pkl")
    scaler = joblib.load("feature_scaler.pkl")
    metadata = joblib.load("model_metadata.pkl")
    return model, label_encoders, feature_names, scaler, metadata

try:
    model, label_encoders, feature_names, scaler, metadata = load_artifacts()
except Exception as e:
    st.error("❌ Failed to load model artifacts. Please ensure model files exist.")
    st.stop()

# ============================
# ⚙️ Helper: Preprocessing
# ============================
def preprocess_case(df):
    df = df.copy()

    drop_cols = ["case_id", "cnr_number", "fir_number"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")

    # Handle dates
    date_cols = ["filed_date", "last_hearing_date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df[f'{col}_year'] = df[col].dt.year
            df[f'{col}_month'] = df[col].dt.month
            df[f'{col}_dayofweek'] = df[col].dt.dayofweek
            df[f'{col}_quarter'] = df[col].dt.quarter
            df[f'{col}_days'] = (df[col] - pd.Timestamp("2000-01-01")).dt.days
            df = df.drop(columns=[col])

    # Derived features
    if 'case_age_days' in df.columns and 'adjournments_count' in df.columns:
        df['delay_per_adjournment'] = df['case_age_days'] / (df['adjournments_count'] + 1)

    if 'undertrial_duration_months' in df.columns and 'evidence_complexity_score' in df.columns:
        df['complexity_duration_ratio'] = df['evidence_complexity_score'] * df['undertrial_duration_months']

    if 'number_of_petitioners' in df.columns and 'number_of_respondents' in df.columns:
        df['total_parties'] = df['number_of_petitioners'] + df['number_of_respondents']
        df['party_ratio'] = df['number_of_petitioners'] / (df['number_of_respondents'] + 1)

    # Fill missing numeric values
    for col in df.select_dtypes(include=["float", "int"]).columns:
        df[col] = df[col].fillna(df[col].median())

    # Fill missing categorical values
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].fillna("Unknown")
        if col in label_encoders:
            le = label_encoders[col]
            df[col] = df[col].apply(lambda x: x if x in le.classes_ else "Unknown")
            df[col] = le.transform(df[col].astype(str))
        else:
            df[col] = pd.factorize(df[col])[0]

    for feat in feature_names:
        if feat not in df.columns:
            df[feat] = 0

    return df[feature_names]

# ============================
# 🔮 Prediction Function
# ============================
def predict_priority(df):
    X = preprocess_case(df)
    preds = model.predict(X)
    probs = model.predict_proba(X)

    priority_map = {
        0: 'Very Low Priority',
        1: 'Low Priority',
        2: 'Medium Priority',
        3: 'High Priority',
        4: 'Critical Priority'
    }

    results = pd.DataFrame({
        'case_id': df.get('case_id', pd.Series(range(len(df)))),
        'predicted_priority': [priority_map.get(p, "Unknown") for p in preds],
        'priority_class': preds,
        'confidence': probs.max(axis=1)
    })

    # Add all class probabilities dynamically
    for i in range(probs.shape[1]):
        results[f'class_{i}_prob'] = probs[:, i]

    return results

# ============================
# 🎨 Streamlit UI
# ============================
st.title("⚖️ Court Case Priority Prediction Dashboard")
st.markdown("""
This dashboard predicts **priority levels** of court cases using AI.  
Upload case data (CSV) to see predicted priority levels instantly.
""")

st.sidebar.header("📁 Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Upload `court_cases.csv`", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded {len(df)} cases from CSV.")
    st.write("### 🧾 Input Data Preview")
    st.dataframe(df.head())

    if st.button("🔮 Predict Priorities"):
        with st.spinner("Predicting priorities... Please wait ⏳"):
            results = predict_priority(df)
            st.success("✅ Prediction complete!")

            # Display results
            st.subheader("📊 Predicted Results")
            st.dataframe(results)

            # Priority Distribution
            st.subheader("📈 Priority Distribution")
            fig = px.pie(
                results,
                names="predicted_priority",
                title="Predicted Priority Distribution",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(fig, use_container_width=True)

            # Confidence Histogram
            st.subheader("🎯 Confidence Levels")
            fig2 = px.histogram(
                results,
                x="confidence",
                nbins=20,
                title="Model Confidence Distribution",
                color="predicted_priority",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Download Button
            csv = results.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Predictions as CSV",
                data=csv,
                file_name="predicted_priorities.csv",
                mime="text/csv"
            )

else:
    st.info("👆 Please upload a CSV file to start predictions.")

# ============================
# 🧠 About Section
# ============================
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 Model Information")
st.sidebar.write(f"**Model Type:** {metadata['model_type']}")
st.sidebar.write(f"**Accuracy:** {metadata['accuracy']:.4f}")
st.sidebar.write(f"**Features Used:** {metadata['n_features']}")
st.sidebar.write(f"**Simplified Target:** {metadata['simplified_target']}")

st.sidebar.markdown("---")
st.sidebar.caption("Developed with ❤️ for JusticeAI – Court Case Prioritizer")
