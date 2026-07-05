import os

import requests

from dotenv import load_dotenv
from api import country_fetcher


API_URL = "http://www.omdbapi.com/"

# Load variables from the .env file.
load_dotenv()

# Read the OMDb API key from the environment.
API_KEY = os.getenv("OMDB_API_KEY")


def fetch_movie_data(movie_title):
    """
    Fetch movie data from the OMDb API.
    Returns a dictionary with the movie data if the movie was found:
    {
        "title": ...,
        "year": ...,
        "rating": ...,
        "poster_url": ...
    }
    Returns None if the movie was not found or the API request failed.
    """

    # Stop the request if no API key was found.
    if not API_KEY:
        print("API key is missing. Please add OMDB_API_KEY to the .env file.")
        return None

    # Send the API key and movie title as GET parameters.
    params = {
        "apikey": API_KEY,
        "t": movie_title,
    }

    try:
        # Send the request to the OMDb API.
        response = requests.get(API_URL, params=params)

    except requests.exceptions.RequestException:
        # This runs if the API request fails,
        # for example because there is no internet connection.
        print("Could not connect to the OMDb API.")
        return None

    # Stop if the API returns an unexpected status code.
    if response.status_code != 200:
        print(f"API request failed with status code {response.status_code}.")
        return None

    # Convert the JSON response into Python data.
    movie_data = response.json()

    if movie_data.get("Response") == "False":
        # The API was reached, but it did not find a movie with this title.
        print(f'Movie "{movie_title}" was not found.')
        return None

    # Stop if the movie has no usable IMDb rating.
    if movie_data.get("imdbRating") == "N/A":
        print(f'Movie "{movie_title}" has no IMDb rating.')
        return None

    country_info = country_fetcher.fetch_flag_data(
        movie_data.get("Country", "")
    )

    poster_url = movie_data.get("Poster", "")

    if poster_url == "N/A":
        poster_url = ""

    # Keep only the values that our app needs.
    movie = {
        "title": movie_data["Title"],
        "year": int(movie_data["Year"][:4]),
        "rating": float(movie_data["imdbRating"]),
        "poster_url": poster_url,
        "imdb_url": f'https://www.imdb.com/title/{movie_data["imdbID"]}/',
        "country": country_info["country"],
        "flag_url": country_info["flag_url"],
    }

    return movie


if __name__ == "__main__":
    # Simple manual tests for this file.
    print(fetch_movie_data("Titanic"))
    print(fetch_movie_data("dsffsadfdewq"))