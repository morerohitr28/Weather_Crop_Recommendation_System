# Final crop recommendation module


def generate_recommendation(
    farmer_details,
    predicted_crop,
    rainfall_result,
    image_quality_result=None
):
    """
    Generate the final recommendation using:
    - Farmer and farm details
    - Predicted crop
    - Rainfall risk
    - Image quality result
    """

    recommendation = {
        "farmer": farmer_details.get("farmer_name", "N/A"),
        "location": farmer_details.get("location", "N/A"),
        "farm_area": farmer_details.get("farm_area", "N/A"),
        "recommended_crop": predicted_crop,
        "rainfall_category": rainfall_result.get("category", "Unknown"),
        "rainfall_risk": rainfall_result.get("risk_level", "Unknown"),
        "rainfall_advice": rainfall_result.get("recommendation", "")
    }

    # Add image quality information if available
    if image_quality_result:
        recommendation["image_quality"] = image_quality_result.get(
            "status", "Unknown"
        )
        recommendation["image_message"] = image_quality_result.get(
            "message", ""
        )

    # Final advice based on rainfall risk
    if rainfall_result.get("risk_level") == "High":
        recommendation["final_advice"] = (
            f"{predicted_crop} is the predicted suitable crop. "
            "However, rainfall conditions require additional attention. "
            "Follow proper irrigation or drainage practices as appropriate."
        )
    else:
        recommendation["final_advice"] = (
            f"{predicted_crop} is the predicted suitable crop "
            "based on the provided soil and weather parameters."
        )

    return recommendation