from sqlalchemy import create_engine, text


# The database file is stored in the data folder.
# This keeps database files separate from the Python code.
DB_URL = "sqlite:///data/movies.db"

# Create the database connection.
# echo=False keeps the terminal output clean.
engine = create_engine(DB_URL, echo=False)


# Create the users and movies tables if they do not exist yet.
with engine.connect() as connection:
    # The users table stores all available user profiles.
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """))

    # Each movie belongs to one user through the user_id column.
    # The same movie title can exist for different users,
    # but only once per user.
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT,
            UNIQUE(title, user_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """))

    connection.commit()


def list_users():
    """
    Retrieve all users from the database.
    Returns a dictionary with user IDs as keys and user names as values.
    """

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id, name FROM users ORDER BY name")
        )
        users = result.fetchall()

    return {
        row[0]: row[1]
        for row in users
    }


def add_user(name):
    """
    Add a new user profile to the database.
    """

    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO users (name) VALUES (:name)"),
                {
                    "name": name
                }
            )
            connection.commit()

        except Exception as error:
            print(f"Error: {error}")


def get_user_id(name):
    """
    Return the ID of a user by name.
    Returns None if the user does not exist.
    """

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id FROM users WHERE name = :name"),
            {
                "name": name
            }
        )
        user = result.fetchone()

    # If no user was found, fetchone() returns None.
    if user is None:
        return None

    return user[0]


def list_movies(user_id):
    """
    Retrieve all movies for one user from the database.
    Returns the movies in the structure used by movies.py.
    """

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT title, year, rating, poster_url
                FROM movies
                WHERE user_id = :user_id
            """),
            {
                "user_id": user_id
            }
        )
        movies = result.fetchall()

    return {
        row[0]: {
            "year": row[1],
            "rating": row[2],
            "poster_url": row[3]
        }
        for row in movies
    }


def add_movie(user_id, title, year, rating, poster_url):
    """
    Add a new movie to one user's movie collection.
    """

    with engine.connect() as connection:
        try:
            connection.execute(
                text("""
                    INSERT INTO movies (user_id, title, year, rating, poster_url)
                    VALUES (:user_id, :title, :year, :rating, :poster_url)
                """),
                {
                    "user_id": user_id,
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "poster_url": poster_url
                }
            )
            connection.commit()

        except Exception as error:
            print(f"Error: {error}")


def delete_movie(user_id, title):
    """
    Delete a movie from one user's movie collection.
    """

    with engine.connect() as connection:
        try:
            # user_id makes sure that only the active user's movie is deleted.
            connection.execute(
                text("""
                    DELETE FROM movies
                    WHERE user_id = :user_id
                    AND title = :title
                """),
                {
                    "user_id": user_id,
                    "title": title
                }
            )
            connection.commit()

        except Exception as error:
            print(f"Error: {error}")


def update_movie(user_id, title, rating):
    """
    Update a movie rating in one user's movie collection.
    """

    with engine.connect() as connection:
        try:
            # user_id makes sure that only the active user's movie is updated.
            connection.execute(
                text("""
                    UPDATE movies
                    SET rating = :rating
                    WHERE user_id = :user_id
                    AND title = :title
                """),
                {
                    "user_id": user_id,
                    "title": title,
                    "rating": rating
                }
            )
            connection.commit()

        except Exception as error:
            print(f"Error: {error}")