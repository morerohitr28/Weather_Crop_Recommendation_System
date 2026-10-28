import streamlit as st
from pathlib import Path
import pickle
import pandas as pd

from modules.farmer import get_farmer_details
from modules.image_quality import check_image_quality
from modules.soil import analyze_soil
from modules.weather import analyze_weather
from modules.rainfall_risk import calculate_rainfall_risk
from modules.recommendation import generate_recommendation
from utils.validation import (
    validate_soil_parameters,
    validate_weather_parameters,
    validate_farmer_details
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "crop_model.pkl"
ENCODER_PATH = BASE_DIR / "models" / "label_encoder.pkl"

LAND_UPLOAD_DIR = BASE_DIR / "uploads" / "land"
SOIL_UPLOAD_DIR = BASE_DIR / "uploads" / "soil"

LAND_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SOIL_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AgriSmart - Crop Recommendation",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f5f9f5;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #174d2b;
    }

    .hero {
        background: linear-gradient(135deg, #176b36, #2e8b57);
        padding: 35px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 18px;
        margin: 0;
    }

    .crop-result {
        background: linear-gradient(135deg, #e8f7e8, #d3f0d3);
        border: 2px solid #2e8b57;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 25px;
    }

    .crop-result h1 {
        font-size: 42px;
        color: #176b36;
        margin: 10px 0;
    }

    .crop-result p {
        font-size: 17px;
        color: #355e3b;
    }

    .top-crop {
        border: 1px solid #cfe4d2;
        border-radius: 18px;
        padding: 25px;
        text-align: center;
        background: white;
        min-height: 220px;
    }

    .top-crop h2 {
        color: #176b36;
        margin-bottom: 10px;
    }

    .rank {
        font-size: 20px;
        font-weight: bold;
        color: #2e8b57;
    }

    .crop-name {
        font-size: 25px;
        font-weight: bold;
        color: #174d2b;
        margin: 15px 0;
    }

    .confidence {
        font-size: 18px;
        color: #4f6f52;
    }

    .section-box {
        background: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #dce9df;
        margin-bottom: 20px;
    }

    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #dce9df;
    }

    .metric-title {
        font-size: 14px;
        color: #667766;
        font-weight: bold;
        text-transform: uppercase;
    }

    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #176b36;
        margin-top: 8px;
    }

    .footer {
        text-align: center;
        color: #6b7d70;
        margin-top: 50px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "farmer_details" not in st.session_state:
    st.session_state.farmer_details = None

if "soil_result" not in st.session_state:
    st.session_state.soil_result = None

if "weather_result" not in st.session_state:
    st.session_state.weather_result = None

if "rainfall_result" not in st.session_state:
    st.session_state.rainfall_result = None

if "image_quality_result" not in st.session_state:
    st.session_state.image_quality_result = None

if "top_crops" not in st.session_state:
    st.session_state.top_crops = None

if "recommendation" not in st.session_state:
    st.session_state.recommendation = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.image(
        "assets/logo.png",
        use_container_width=True
    )

    st.title("🌱 AgriSmart")

    st.caption(
        "Weather & Soil-Based Crop Recommendation System"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "👨‍🌾 Farmer & Farm",
            "🌱 Soil Analysis",
            "🌦️ Weather Analysis",
            "🌾 Crop Recommendation"
        ]
    )

    st.divider()

    st.info(
        "Enter soil-test and weather values to receive "
        "AI-based crop recommendations."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🌱 AgriSmart</h1>
        <p>Weather & Soil-Based Crop Recommendation System</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PAGE 1 - FARMER
# ============================================================

if page == "👨‍🌾 Farmer & Farm":

    st.header("👨‍🌾 Farmer & Farm Details")

    st.write(
        "Enter the basic details of the farmer and farm."
    )

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            farmer_name = st.text_input(
                "Farmer Name",
                placeholder="Enter farmer name"
            )

            location = st.text_input(
                "Location",
                placeholder="Example: Pune, Maharashtra"
            )

        with col2:

            farm_area = st.number_input(
                "Farm Area (acres)",
                min_value=0.1,
                value=1.0,
                step=0.1
            )

            soil_type = st.selectbox(
                "Soil Type",
                [
                    "Select",
                    "Black Soil",
                    "Red Soil",
                    "Alluvial Soil",
                    "Loamy Soil",
                    "Sandy Soil",
                    "Clay Soil",
                    "Other"
                ]
            )

    st.subheader("📷 Land Image")

    land_image = st.file_uploader(
        "Upload a clear image of your farmland",
        type=["jpg", "jpeg", "png"],
        key="land_image"
    )

    st.subheader("🧪 Soil Image")

    soil_image = st.file_uploader(
        "Upload a clear image of your soil",
        type=["jpg", "jpeg", "png"],
        key="soil_image"
    )

    if st.button(
        "💾 Save Farmer Details",
        type="primary",
        use_container_width=True
    ):

        validation = validate_farmer_details(
            farmer_name,
            location,
            farm_area
        )

        if not validation["valid"]:

            for error in validation["errors"]:
                st.error(error)

        else:

            st.session_state.farmer_details = get_farmer_details(
                farmer_name,
                location,
                farm_area,
                None if soil_type == "Select" else soil_type
            )

            # Save land image
            if land_image is not None:

                land_path = LAND_UPLOAD_DIR / land_image.name

                with open(land_path, "wb") as file:
                    file.write(land_image.getbuffer())

                st.session_state.image_quality_result = (
                    check_image_quality(land_path)
                )

            # Save soil image
            if soil_image is not None:

                soil_path = SOIL_UPLOAD_DIR / soil_image.name

                with open(soil_path, "wb") as file:
                    file.write(soil_image.getbuffer())

            st.success(
                "Farmer and farm details saved successfully."
            )


# ============================================================
# PAGE 2 - SOIL
# ============================================================

elif page == "🌱 Soil Analysis":

    st.header("🌱 Soil Analysis")

    st.write(
        "Enter soil-test values used by the crop prediction model."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        N = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            max_value=300.0,
            value=50.0,
            step=1.0
        )

    with col2:
        P = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            max_value=200.0,
            value=40.0,
            step=1.0
        )

    with col3:
        K = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            max_value=300.0,
            value=40.0,
            step=1.0
        )

    with col4:
        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1
        )

    if st.button(
        "🔬 Analyze Soil",
        type="primary"
    ):

        validation = validate_soil_parameters(
            N, P, K, ph
        )

        if not validation["valid"]:

            for error in validation["errors"]:
                st.error(error)

        else:

            st.session_state.soil_result = analyze_soil(
                N, P, K, ph
            )

            st.success(
                "Soil analysis completed successfully."
            )

    if st.session_state.soil_result:

        result = st.session_state.soil_result

        st.subheader("📊 Soil Dashboard")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Nitrogen",
                result["nitrogen_status"]
            )

        with c2:
            st.metric(
                "Phosphorus",
                result["phosphorus_status"]
            )

        with c3:
            st.metric(
                "Potassium",
                result["potassium_status"]
            )

        with c4:
            st.metric(
                "pH",
                result["ph_status"]
            )

        st.subheader("💡 Soil Guidance")

        for item in result["guidance"]:
            st.info(item)


# ============================================================
# PAGE 3 - WEATHER
# ============================================================

elif page == "🌦️ Weather Analysis":

    st.header("🌦️ Weather Analysis")

    st.write(
        "Enter the current or expected weather conditions."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=-50.0,
            max_value=60.0,
            value=25.0,
            step=0.5
        )

    with col2:

        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=1.0
        )

    with col3:

        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            max_value=1000.0,
            value=100.0,
            step=1.0
        )

    if st.button(
        "🌦️ Analyze Weather",
        type="primary"
    ):

        validation = validate_weather_parameters(
            temperature,
            humidity,
            rainfall
        )

        if not validation["valid"]:

            for error in validation["errors"]:
                st.error(error)

        else:

            st.session_state.weather_result = analyze_weather(
                temperature,
                humidity,
                rainfall
            )

            st.session_state.rainfall_result = (
                calculate_rainfall_risk(rainfall)
            )

            st.success(
                "Weather analysis completed successfully."
            )

    if st.session_state.weather_result:

        result = st.session_state.weather_result

        st.subheader("🌤️ Weather Dashboard")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Temperature",
                f"{result['temperature']:.1f} °C"
            )

            st.caption(
                result["temperature_status"]
            )

        with c2:
            st.metric(
                "Humidity",
                f"{result['humidity']:.1f} %"
            )

            st.caption(
                result["humidity_status"]
            )

        with c3:
            st.metric(
                "Rainfall",
                f"{result['rainfall']:.1f} mm"
            )

            st.caption(
                result["rainfall_status"]
            )

        st.subheader("💡 Weather Guidance")

        for item in result["guidance"]:
            st.info(item)

        if st.session_state.rainfall_result:

            rr = st.session_state.rainfall_result

            st.subheader("🌧️ Rainfall Risk")

            if rr["risk_level"] == "High":
                st.warning(
                    f"Rainfall Category: {rr['category']} | "
                    f"Risk: {rr['risk_level']}"
                )
            else:
                st.success(
                    f"Rainfall Category: {rr['category']} | "
                    f"Risk: {rr['risk_level']}"
                )


# ============================================================
# PAGE 4 - CROP RECOMMENDATION
# ============================================================

elif page == "🌾 Crop Recommendation":

    st.header("🌾 Crop Recommendation")

    st.write(
        "The Random Forest model ranks crops according to "
        "their predicted probability."
    )

    # --------------------------------------------------------
    # Check required information
    # --------------------------------------------------------

    if st.session_state.farmer_details is None:

        st.warning(
            "Please save Farmer & Farm details first."
        )

        st.stop()

    if st.session_state.soil_result is None:

        st.warning(
            "Please complete Soil Analysis first."
        )

        st.stop()

    if st.session_state.weather_result is None:

        st.warning(
            "Please complete Weather Analysis first."
        )

        st.stop()

    farmer = st.session_state.farmer_details
    soil = st.session_state.soil_result
    weather = st.session_state.weather_result

    # --------------------------------------------------------
    # INPUT SUMMARY
    # --------------------------------------------------------

    st.subheader("📋 Input Summary")

    c1, c2, c3 = st.columns(3)

    with c1:

        with st.container(border=True):

            st.markdown("### 👨‍🌾 FARMER")

            st.write(
                f"**Name:** {farmer['farmer_name']}"
            )

            st.write(
                f"**Location:** {farmer['location']}"
            )

            st.write(
                f"**Farm Area:** {farmer['farm_area']} acres"
            )

            if farmer.get("soil_type"):
                st.write(
                    f"**Soil Type:** {farmer['soil_type']}"
                )

    with c2:

        with st.container(border=True):

            st.markdown("### 🌱 SOIL")

            st.write(
                f"**N:** {soil['N']:.1f}"
            )

            st.write(
                f"**P:** {soil['P']:.1f}"
            )

            st.write(
                f"**K:** {soil['K']:.1f}"
            )

            st.write(
                f"**pH:** {soil['pH']:.1f}"
            )

    with c3:

        with st.container(border=True):

            st.markdown("### 🌦️ WEATHER")

            st.write(
                f"**Temperature:** "
                f"{weather['temperature']:.1f} °C"
            )

            st.write(
                f"**Humidity:** "
                f"{weather['humidity']:.1f} %"
            )

            st.write(
                f"**Rainfall:** "
                f"{weather['rainfall']:.1f} mm"
            )

    st.divider()

    # --------------------------------------------------------
    # PREDICT TOP 3
    # --------------------------------------------------------

    if st.button(
        "🌾 Predict Top 3 Suitable Crops",
        type="primary",
        use_container_width=True
    ):

        try:

            # Check model files

            if not MODEL_PATH.exists():

                st.error(
                    f"Model file not found:\n{MODEL_PATH}"
                )

                st.stop()

            if not ENCODER_PATH.exists():

                st.error(
                    f"Encoder file not found:\n{ENCODER_PATH}"
                )

                st.stop()

            if MODEL_PATH.stat().st_size == 0:

                st.error(
                    "crop_model.pkl is empty. "
                    "Please retrain the model."
                )

                st.stop()

            if ENCODER_PATH.stat().st_size == 0:

                st.error(
                    "label_encoder.pkl is empty. "
                    "Please retrain the model."
                )

                st.stop()

            # Load model

            with open(MODEL_PATH, "rb") as file:
                model = pickle.load(file)

            # Load encoder

            with open(ENCODER_PATH, "rb") as file:
                encoder = pickle.load(file)

            # Prepare input

            input_data = pd.DataFrame(
                [[
                    soil["N"],
                    soil["P"],
                    soil["K"],
                    weather["temperature"],
                    weather["humidity"],
                    soil["pH"],
                    weather["rainfall"]
                ]],
                columns=[
                    "N",
                    "P",
                    "K",
                    "temperature",
                    "humidity",
                    "ph",
                    "rainfall"
                ]
            )

            # Prediction probabilities

            probabilities = model.predict_proba(
                input_data
            )[0]

            # Get top 3 indexes

            top_indices = probabilities.argsort()[-3:][::-1]

            top_crops = []

            for index in top_indices:

                encoded_class = model.classes_[index]

                crop_name = encoder.inverse_transform(
                    [encoded_class]
                )[0]

                confidence = probabilities[index] * 100

                top_crops.append(
                    {
                        "crop": crop_name,
                        "confidence": confidence
                    }
                )

            st.session_state.top_crops = top_crops

            # Best crop

            best_crop = top_crops[0]["crop"]

            rainfall_result = st.session_state.rainfall_result

            if rainfall_result is None:

                rainfall_result = calculate_rainfall_risk(
                    weather["rainfall"]
                )

            st.session_state.recommendation = (
                generate_recommendation(
                    farmer,
                    best_crop,
                    rainfall_result,
                    st.session_state.image_quality_result
                )
            )

            st.success(
                "Top 3 crop prediction completed successfully."
            )

        except Exception as error:

            st.error(
                f"Prediction failed: {error}"
            )

    # --------------------------------------------------------
    # TOP 3 DISPLAY
    # --------------------------------------------------------

    if st.session_state.top_crops:

        st.subheader("🏆 Top 3 Crop Recommendations")

        st.caption(
            "Crops are ranked according to the probability "
            "produced by the trained Random Forest model."
        )

        crops = st.session_state.top_crops

        columns = st.columns(3)

        medals = ["🥇", "🥈", "🥉"]

        for i, crop_data in enumerate(crops):

            with columns[i]:

                with st.container(border=True):

                    st.markdown(
                        f"## {medals[i]}"
                    )

                    st.markdown(
                        f"### Rank {i + 1}"
                    )

                    st.markdown(
                        f"## 🌾 {crop_data['crop'].title()}"
                    )

                    st.metric(
                        "Confidence",
                        f"{crop_data['confidence']:.1f}%"
                    )

                    # Progress bar

                    st.progress(
                        min(
                            crop_data["confidence"] / 100,
                            1.0
                        )
                    )

        # ----------------------------------------------------
        # BEST CROP
        # ----------------------------------------------------

        best = crops[0]

        st.markdown(
            f"""
            <div class="crop-result">
                <div style="font-size:55px;">🌾</div>
                <p><b>BEST RECOMMENDED CROP</b></p>
                <h1>{best['crop'].title()}</h1>
                <p>
                    Random Forest confidence:
                    <b>{best['confidence']:.1f}%</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # RECOMMENDATION DETAILS
        # ----------------------------------------------------

        if st.session_state.recommendation:

            recommendation = st.session_state.recommendation

            st.subheader("💡 Recommendation Details")

            c1, c2, c3 = st.columns(3)

            with c1:

                with st.container(border=True):

                    st.markdown("### 🌧️ RAINFALL")

                    st.metric(
                        "Category",
                        recommendation[
                            "rainfall_category"
                        ]
                    )

                    st.write(
                        "Risk:",
                        recommendation[
                            "rainfall_risk"
                        ]
                    )

            with c2:

                with st.container(border=True):

                    st.markdown("### 📷 IMAGE QUALITY")

                    image_quality = recommendation.get(
                        "image_quality",
                        "Not provided"
                    )

                    st.metric(
                        "Status",
                        image_quality
                    )

            with c3:

                with st.container(border=True):

                    st.markdown("### 🌾 BEST CROP")

                    st.metric(
                        "Crop",
                        recommendation[
                            "recommended_crop"
                        ].title()
                    )

            st.subheader("🌱 Final Advice")

            st.info(
                recommendation["final_advice"]
            )

            st.subheader("🌧️ Rainfall Advice")

            st.write(
                recommendation["rainfall_advice"]
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🌱 <b>AgriSmart</b> |
        Weather & Soil-Based Crop Recommendation System<br>
        Powered by Streamlit & Random Forest Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)