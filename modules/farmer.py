# Farmer and farm details module


def get_farmer_details(
    farmer_name,
    location,
    farm_area,
    soil_type=None
):
    """
    Store and return basic farmer and farm details.
    """

    farmer_details = {
        "farmer_name": farmer_name,
        "location": location,
        "farm_area": farm_area,
        "soil_type": soil_type
    }

    return farmer_details