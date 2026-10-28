import cv2
import numpy as np


def check_image_quality(image_path):
    """
    Check the quality of a soil/land image.

    Returns:
        dict: Image quality information including
              brightness, sharpness, resolution, and status.
    """

    # Read image
    image = cv2.imread(str(image_path))

    if image is None:
        return {
            "status": "Invalid",
            "message": "Unable to read the image."
        }

    # Get image dimensions
    height, width = image.shape[:2]

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate brightness
    brightness = float(np.mean(gray))

    # Calculate sharpness using Laplacian variance
    sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    # Basic resolution check
    resolution_ok = width >= 300 and height >= 300

    # Brightness check
    brightness_ok = 40 <= brightness <= 220

    # Sharpness check
    sharpness_ok = sharpness >= 50

    # Final quality decision
    if resolution_ok and brightness_ok and sharpness_ok:
        status = "Good"
        message = "Image quality is suitable for further analysis."

    else:
        status = "Poor"
        message = "Image quality is poor. Please upload a clearer image."

    return {
        "status": status,
        "message": message,
        "width": width,
        "height": height,
        "brightness": round(brightness, 2),
        "sharpness": round(sharpness, 2)
    }