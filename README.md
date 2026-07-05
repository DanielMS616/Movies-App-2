<p align="center">
  <img src="docs/readme_header.svg" alt="Movie Vault Header" width="100%">
</p>

Movie Vault is a Python movie collection app with a terminal menu, SQLite database storage, API integration and a generated HTML website.

The app allows different users to create their own personal movie collections. Movie data is fetched automatically from the OMDb API, enriched with country and flag data, saved in a local SQLite database and displayed on a generated website.

## Features

- Create and switch between user profiles
- Add movies by entering only the movie title
- Fetch movie data from the OMDb API
- Fetch country and flag data from API Ninjas
- Store movies in a local SQLite database
- Save user-specific movie collections
- Add personal notes to movies
- Show notes as poster tooltips on the website
- Generate an HTML website from the movie database
- Show movie posters, year, rating, country and flag
- Link movie posters to IMDb pages
- Use a fallback poster if no poster is available
- Search, filter and sort movies on the generated website

## Technologies Used

- Python
- SQLite
- SQLAlchemy
- Requests
- python-dotenv
- Matplotlib
- Pyfiglet
- HTML
- CSS
- JavaScript
- OMDb API
- API Ninjas Country API
- API Ninjas Country Flag API

## Project Structure

```text
movieproject2/
├── api/
│   ├── __init__.py
│   ├── country_fetcher.py
│   └── movie_fetcher.py
├── data/
│   └── .gitkeep
├── docs/
│   └── readme_header.svg
├── static/
│   ├── no_poster.png
│   ├── script.js
│   └── style.css
├── storage/
│   ├── __init__.py
│   └── movie_storage_sql.py
├── templates/
│   └── index_template.html
├── index.html
├── movies.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Main Files and Folders

### `movies.py`

This is the main file of the application.

It contains the terminal menu and connects the user input with the different app functions.

### `api/`

This folder contains files that fetch data from external APIs.

- `movie_fetcher.py` fetches movie data from the OMDb API.
- `country_fetcher.py` fetches country and flag information from API Ninjas.

### `storage/`

This folder contains the database logic.

- `movie_storage_sql.py` creates the database tables and handles all database actions.

### `data/`

This folder is used for the local SQLite database.

The actual database file is ignored by Git and is not uploaded to GitHub.

### `static/`

This folder contains static website files.

- `style.css` styles the generated website.
- `script.js` adds search, filter and sorting functions.
- `no_poster.png` is used when no movie poster is available.

### `templates/`

This folder contains the HTML template that is used to generate the final website.

## Setup

Clone the repository:

```bash
git clone <your-repository-url>
cd movieproject2
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OMDB_API_KEY=your_omdb_api_key
API_NINJAS_API_KEY=your_api_ninjas_key
```

The `.env` file contains private API keys and must not be committed to GitHub.

## How to Run the App

Start the app with:

```bash
python3 movies.py
```

The app starts with a user selection menu.

You can select an existing user or create a new user profile.

After that, the main menu is shown.

## Main Menu

The terminal menu includes options like:

```text
0. Exit
1. List movies
2. Add new movie
3. Delete movie
4. Update movie note
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Create rating histogram
10. Movies sorted by year
11. Filter movies
12. Generate website
13. Switch user
```

## User Profiles

Each user has their own movie collection.

When the app starts, the user can select an existing profile or create a new one.

Movies are connected to users in the database with a `user_id`. This makes sure that users only see and edit their own movie collection.

User names are normalized before saving. For example:

```text
sara
 Sara
SARA
```

are handled as:

```text
Sara
```

## Website Generation

The app can generate an `index.html` file from the movies stored in the database.

To generate the website, choose option `12` in the terminal menu.

The generated website includes:

- movie posters
- movie titles
- release years
- IMDb ratings
- country flags
- IMDb links
- movie search
- country filter
- sorting by title, year or rating
- fallback poster for movies without poster image

## Movie Notes

Users can add a personal note to a movie.

The note is stored in the database and displayed as a tooltip when hovering over the movie poster on the generated website.

## Database

The app uses SQLite with SQLAlchemy.

There are two main tables:

### `users`

Stores user profiles.

### `movies`

Stores movies and connects each movie to a user by using a `user_id`.

This makes it possible for each user to have their own personal movie collection.

## APIs

### OMDb API

The OMDb API is used to fetch movie information such as:

- title
- year
- IMDb rating
- poster URL
- IMDb ID
- country

### API Ninjas

API Ninjas is used to fetch country and flag information.

The country data is used to display a small flag next to each movie on the generated website.

## Notes About Git

The following files are intentionally not uploaded to GitHub:

- `.env`
- `data/movies.db`
- `.venv/`
- `__pycache__/`
- test files
- IDE settings

The database is local because it contains user-specific app data.

The `.env` file is local because it contains private API keys.

## Contributing

This is a school project, but suggestions and improvements are welcome.