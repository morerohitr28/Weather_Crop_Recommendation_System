# Data preprocessing utilities for the
# Weather & Soil-Based Crop Recommendation System

import pandas as pd
from sklearn.preprocessing import LabelEncoder


FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]


def load_crop_data(file_path):
    """
    Load the crop dataset from a CSV file.
    """
    return pd.read_csv(file_path)


def clean_crop_data(df):
    """
    Clean the crop dataset by removing duplicates
    and handling missing values.
    """

    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing numerical values with median
    for column in FEATURES:
        if column in df.columns:
            df[column] = df[column].fillna(df[column].median())

    return df


def prepare_features(df):
    """
    Extract the input features used by the crop model.
    """

    missing_features = [
        feature for feature in FEATURES
        if feature not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    return df[FEATURES].copy()


def encode_labels(labels):
    """
    Encode crop names into numerical labels.

    Returns:
        encoded_labels: Numerical labels
        label_encoder: Fitted LabelEncoder
    """

    label_encoder = LabelEncoder()

    encoded_labels = label_encoder.fit_transform(labels)

    return encoded_labels, label_encoder


def preprocess_crop_data(df):
    """
    Complete preprocessing pipeline for crop data.

    Returns:
        X: Input features
        y: Encoded crop labels
        label_encoder: Fitted label encoder
    """

    df = clean_crop_data(df)

    X = prepare_features(df)

    y, label_encoder = encode_labels(df["label"])

    return X, y, label_encoder