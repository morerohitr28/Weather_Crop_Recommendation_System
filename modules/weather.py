# Weather analysis module


def analyze_weather(temperature, humidity, rainfall):
    """
    Analyze basic weather parameters and provide
    simple agricultural guidance.

    Parameters:
        temperature : Temperature in Celsius
        humidity    : Relative humidity in percentage
        rainfall    : Rainfall in mm

    Returns:
        dict: Weather status and guidance
    """

    temperature = float(temperature)
    humidity = float(humidity)
    rainfall = float(rainfall)

    # Temperature status
    if temperature < 15:
        temperature_status = "Low"
    elif temperature <= 35:
        temperature_status = "Suitable"
    else:
        temperature_status = "High"

    # Humidity status
    if humidity < 40:
        humidity_status = "Low"
    elif humidity <= 80:
        humidity_status = "Suitable"
    else:
        humidity_status = "High"

    # Rainfall status
    if rainfall < 50:
        rainfall_status = "Low"
    elif rainfall <= 200:
        rainfall_status = "Normal"
    else:
        rainfall_status = "High"

    # Weather guidance
    guidance = []

    if temperature_status == "Low":
        guidance.append(
            "Temperature is low. Consider crops suitable for cooler conditions."
        )

    elif temperature_status == "High":
        guidance.append(
            "Temperature is high. Monitor crop water requirements and heat stress."
        )

    if humidity_status == "Low":
        guidance.append(
            "Humidity is low. Monitor soil moisture and irrigation requirements."
        )

    elif humidity_status == "High":
        guidance.append(
            "Humidity is high. Monitor the crop for conditions favorable to diseases."
        )

    if rainfall_status == "Low":
        guidance.append(
            "Rainfall is low. Irrigation may be required depending on the crop and soil."
        )

    elif rainfall_status == "High":
        guidance.append(
            "Rainfall is high. Ensure proper field drainage to reduce waterlogging."
        )

    if not guidance:
        guidance.append(
            "Weather conditions are within the defined suitable ranges."
        )

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "temperature_status": temperature_status,
        "humidity_status": humidity_status,
        "rainfall_status": rainfall_status,
        "guidance": guidance
    }