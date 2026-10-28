from pathlib import Path
import pickle
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "crop_model.pkl"
ENCODER_PATH = BASE_DIR / "models" / "label_encoder.pkl"

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

with open(ENCODER_PATH, "rb") as file:
    label_encoder = pickle.load(file)


FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]


def prepare_input(
    N,
    P,
    K,
    temperature,
    humidity,
    ph,
    rainfall
):
    return pd.DataFrame(
        [[
            N,
            P,
            K,
            temperature,
            humidity,
            ph,
            rainfall
        ]],
        columns=FEATURES
    )


def predict_crop(
    N,
    P,
    K,
    temperature,
    humidity,
    ph,
    rainfall
):
    input_data = prepare_input(
        N,
        P,
        K,
        temperature,
        humidity,
        ph,
        rainfall
    )

    prediction = model.predict(input_data)[0]

    crop_name = label_encoder.inverse_transform(
        [prediction]
    )[0]

    return crop_name


def predict_top_crops(
    N,
    P,
    K,
    temperature,
    humidity,
    ph,
    rainfall,
    top_n=3
):
    """
    Return the top N crop recommendations
    with their prediction probabilities.
    """

    input_data = prepare_input(
        N,
        P,
        K,
        temperature,
        humidity,
        ph,
        rainfall
    )

    probabilities = model.predict_proba(input_data)[0]

    class_indices = probabilities.argsort()[::-1][:top_n]

    results = []

    for index in class_indices:

        crop_name = label_encoder.inverse_transform(
            [model.classes_[index]]
        )[0]

        probability = probabilities[index] * 100

        results.append({
            "crop": crop_name,
            "confidence": round(probability, 2)
        })

    return results