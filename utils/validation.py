# Input validation utilities for the
# Weather & Soil-Based Crop Recommendation System


def validate_soil_parameters(N, P, K, ph):
    """
    Validate soil parameters before crop prediction.
    """

    errors = []

    try:
        N = float(N)
        P = float(P)
        K = float(K)
        ph = float(ph)
    except (TypeError, ValueError):
        return {
            "valid": False,
            "errors": ["Soil parameters must be numeric."]
        }

    if N < 0:
        errors.append("Nitrogen (N) cannot be negative.")

    if P < 0:
        errors.append("Phosphorus (P) cannot be negative.")

    if K < 0:
        errors.append("Potassium (K) cannot be negative.")

    if ph < 0 or ph > 14:
        errors.append("Soil pH must be between 0 and 14.")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_weather_parameters(temperature, humidity, rainfall):
    """
    Validate weather parameters before analysis.
    """

    errors = []

    try:
        temperature = float(temperature)
        humidity = float(humidity)
        rainfall = float(rainfall)
    except (TypeError, ValueError):
        return {
            "valid": False,
            "errors": ["Weather parameters must be numeric."]
        }

    if humidity < 0 or humidity > 100:
        errors.append("Humidity must be between 0 and 100%.")

    if rainfall < 0:
        errors.append("Rainfall cannot be negative.")

    if temperature < -50 or temperature > 60:
        errors.append(
            "Temperature must be between -50°C and 60°C."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_farm_area(farm_area):
    """
    Validate farm area.
    """

    try:
        farm_area = float(farm_area)
    except (TypeError, ValueError):
        return {
            "valid": False,
            "errors": ["Farm area must be numeric."]
        }

    if farm_area <= 0:
        return {
            "valid": False,
            "errors": ["Farm area must be greater than 0."]
        }

    return {
        "valid": True,
        "errors": []
    }


def validate_farmer_details(farmer_name, location, farm_area):
    """
    Validate basic farmer and farm information.
    """

    errors = []

    if not farmer_name or not str(farmer_name).strip():
        errors.append("Farmer name is required.")

    if not location or not str(location).strip():
        errors.append("Location is required.")

    area_result = validate_farm_area(farm_area)

    if not area_result["valid"]:
        errors.extend(area_result["errors"])

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }