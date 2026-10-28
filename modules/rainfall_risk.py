# Rainfall risk analysis module


def calculate_rainfall_risk(rainfall):
    """
    Classify rainfall into Low, Normal, or High risk.

    Parameters:
        rainfall (float): Expected rainfall in mm.

    Returns:
        dict: Rainfall category, risk level, and recommendation.
    """

    rainfall = float(rainfall)

    if rainfall < 50:
        category = "Low"
        risk_level = "High"
        recommendation = (
            "Low rainfall is expected. Irrigation may be required "
            "depending on crop and soil conditions."
        )

    elif rainfall <= 200:
        category = "Normal"
        risk_level = "Low"
        recommendation = (
            "Rainfall is within a normal range. "
            "Suitable drainage and regular monitoring are recommended."
        )

    else:
        category = "High"
        risk_level = "High"
        recommendation = (
            "High rainfall is expected. Ensure proper drainage "
            "and monitor the field for waterlogging."
        )

    return {
        "rainfall": rainfall,
        "category": category,
        "risk_level": risk_level,
        "recommendation": recommendation
    }