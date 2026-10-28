# Soil analysis and guidance module


def analyze_soil(N, P, K, ph):
    """
    Analyze basic soil parameters and provide simple guidance.

    Parameters:
        N  : Nitrogen value
        P  : Phosphorus value
        K  : Potassium value
        ph : Soil pH value

    Returns:
        dict: Soil status and guidance
    """

    N = float(N)
    P = float(P)
    K = float(K)
    ph = float(ph)

    # Nutrient status
    if N < 50:
        nitrogen_status = "Low"
    elif N <= 100:
        nitrogen_status = "Normal"
    else:
        nitrogen_status = "High"

    if P < 30:
        phosphorus_status = "Low"
    elif P <= 60:
        phosphorus_status = "Normal"
    else:
        phosphorus_status = "High"

    if K < 30:
        potassium_status = "Low"
    elif K <= 80:
        potassium_status = "Normal"
    else:
        potassium_status = "High"

    # Soil pH status
    if ph < 5.5:
        ph_status = "Acidic"
    elif ph <= 7.5:
        ph_status = "Suitable"
    else:
        ph_status = "Alkaline"

    # General guidance
    guidance = []

    if nitrogen_status == "Low":
        guidance.append(
            "Nitrogen level is low. Consider appropriate nitrogen management."
        )

    if phosphorus_status == "Low":
        guidance.append(
            "Phosphorus level is low. Consider appropriate phosphorus management."
        )

    if potassium_status == "Low":
        guidance.append(
            "Potassium level is low. Consider appropriate potassium management."
        )

    if ph_status == "Acidic":
        guidance.append(
            "Soil is acidic. Soil amendment may be required based on soil-test advice."
        )

    elif ph_status == "Alkaline":
        guidance.append(
            "Soil is alkaline. Suitable soil management may be required."
        )

    if not guidance:
        guidance.append(
            "The provided soil parameters are within the defined ranges."
        )

    return {
        "N": N,
        "P": P,
        "K": K,
        "pH": ph,
        "nitrogen_status": nitrogen_status,
        "phosphorus_status": phosphorus_status,
        "potassium_status": potassium_status,
        "ph_status": ph_status,
        "guidance": guidance
    }