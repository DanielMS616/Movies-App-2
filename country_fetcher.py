import os

import requests
from dotenv import load_dotenv


COUNTRY_API_URL = "https://api.api-ninjas.com/v1/country"
FLAG_API_URL = "https://api.api-ninjas.com/v1/countryflag"

# Load variables from the .env file.
load_dotenv()

# Read the API Ninjas key from the environment.
API_KEY = os.getenv("API_NINJAS_API_KEY")


def get_first_country(country_text):
    """
    Get the first country from the OMDb country text.
    Example: "USA, Mexico" becomes "USA".
    """

    if country_text is None or country_text == "N/A":
        return ""

    countries = country_text.split(",")
    return countries[0].strip()


def fetch_flag_data(country_text):
    """
    Fetch country and flag information.
    Returns a dictionary with the country name and flag URL.
    Returns empty values if the API request fails.
    """

    country_name = get_first_country(country_text)

    if country_name == "":
        return {
            "country": "",
            "flag_url": ""
        }

    if not API_KEY:
        print("API Ninjas key is missing. Please add API_NINJAS_API_KEY to .env.")
        return {
            "country": country_name,
            "flag_url": ""
        }

    headers = {
        "X-Api-Key": API_KEY
    }

    try:
        # First request: get country data and the ISO-2 country code.
        country_response = requests.get(
            COUNTRY_API_URL,
            headers=headers,
            params={"name": country_name}
        )

        if country_response.status_code != 200:
            print("Could not fetch country data.")
            return {
                "country": country_name,
                "flag_url": ""
            }

        country_data = country_response.json()

        if len(country_data) == 0:
            print(f'No country data found for "{country_name}".')
            return {
                "country": country_name,
                "flag_url": ""
            }

        country_code = country_data[0].get("iso2")

        if country_code is None:
            print(f'No country code found for "{country_name}".')
            return {
                "country": country_name,
                "flag_url": ""
            }

        # Second request: get the flag image URL with the ISO-2 country code.
        flag_response = requests.get(
            FLAG_API_URL,
            headers=headers,
            params={"country": country_code}
        )

        if flag_response.status_code != 200:
            print("Could not fetch flag data.")
            return {
                "country": country_name,
                "flag_url": ""
            }

        flag_data = flag_response.json()

        return {
            "country": country_name,
            "flag_url": flag_data.get("rectangle_image_url", "")
        }

    except requests.exceptions.RequestException:
        print("Could not connect to the API Ninjas API.")
        return {
            "country": country_name,
            "flag_url": ""
        }


if __name__ == "__main__":
    print(fetch_flag_data("USA"))
    print(fetch_flag_data("Germany"))