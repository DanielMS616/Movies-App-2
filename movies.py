import random
import difflib
import html
import movie_fetcher

import matplotlib.pyplot as plt
import pyfiglet

from storage import movie_storage_sql as storage


# Terminal colors
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"

FALLBACK_POSTER = "static/no_poster.png"

def main():
    """
    Start the movie database application.
    The user first selects a profile.
    All movie actions are then connected to this active user.
    """

    active_user_id, active_user_name = select_user()

    while True:
        show_menu(active_user_name)
        choice = user_input()

        if choice == 13:
            active_user_id, active_user_name = select_user()
            continue

        keep_running = navigate_menu(choice, active_user_id, active_user_name)

        if keep_running is False:
            break

        input(GREEN + "\nDrücke Enter, um zum Menü zurückzukehren..." + RESET)


def select_user():
    """
    Let the user select an existing profile or create a new one.
    Returns the selected user's ID and name.
    """

    print(GREEN + BOLD + "\nWelcome to the Movie App!" + RESET)

    while True:
        users = storage.list_users()
        user_items = list(users.items())

        print()
        print(GREEN + "Select a user:" + RESET)

        # Show all existing users with simple menu numbers.
        for index, user in enumerate(user_items, start=1):
            user_id = user[0]
            user_name = user[1]
            print(f"{index}. {user_name}")

        create_choice = len(user_items) + 1
        print(f"{create_choice}. Create new user")

        try:
            choice = int(input(GREEN + "Enter choice: " + RESET))

            if 1 <= choice <= len(user_items):
                selected_user = user_items[choice - 1]
                active_user_id = selected_user[0]
                active_user_name = selected_user[1]

                print(GREEN + f"Welcome back, {active_user_name}!" + RESET)
                return active_user_id, active_user_name

            if choice == create_choice:
                return create_user()

            print(RED + "Invalid choice. Please try again." + RESET)

        except ValueError:
            print(RED + "Please enter a valid number." + RESET)


def create_user():
    """
    Create a new user profile and return the new user's ID and name.
    """

    user_name = get_non_empty_title(GREEN + "Enter new user name: " + RESET)
    user_name = normalize_user_name(user_name)

    # If the user already exists, use the existing profile.
    existing_user_id = storage.get_user_id(user_name)

    if existing_user_id is not None:
        print(GREEN + f"User {user_name} already exists." + RESET)
        return existing_user_id, user_name

    storage.add_user(user_name)
    user_id = storage.get_user_id(user_name)

    print(GREEN + f"User {user_name} created." + RESET)
    return user_id, user_name


def show_menu(active_user_name):
    """
    Display the main menu.
    Shows all available menu options and the active user profile.
    """

    print()

    title = pyfiglet.figlet_format("Movie DB", font="slant")
    print(GREEN + BOLD + title + RESET)

    user_line = f"Aktiver Nutzer: {active_user_name}"

    print(GREEN + "╔════════════════════════════════════╗" + RESET)
    print(GREEN + "║                MENÜ                ║" + RESET)
    print(GREEN + "╠════════════════════════════════════╣" + RESET)
    print(GREEN + f"║ {user_line:<34} ║" + RESET)
    print(GREEN + "╠════════════════════════════════════╣" + RESET)
    print(GREEN + "║ 0. Exit                            ║" + RESET)
    print(GREEN + "║ 1. Alle Filme anzeigen             ║" + RESET)
    print(GREEN + "║ 2. Neuen Film hinzufügen           ║" + RESET)
    print(GREEN + "║ 3. Film aus DB entfernen           ║" + RESET)
    print(GREEN + "║ 4. Filmnotiz anpassen              ║" + RESET)
    print(GREEN + "║ 5. Stats                           ║" + RESET)
    print(GREEN + "║ 6. Zufälliger Film                 ║" + RESET)
    print(GREEN + "║ 7. Filmsuche                       ║" + RESET)
    print(GREEN + "║ 8. Filme nach Bewertung            ║" + RESET)
    print(GREEN + "║ 9. Bewertungs-Histogramm erstellen ║" + RESET)
    print(GREEN + "║ 10. Filme nach Jahr sortieren.     ║" + RESET)
    print(GREEN + "║ 11. Filme filtern                  ║" + RESET)
    print(GREEN + "║ 12. Website generieren             ║" + RESET)
    print(GREEN + "║ 13. Nutzer wechseln                ║" + RESET)
    print(GREEN + "╚════════════════════════════════════╝" + RESET)
    print()


def user_input():
    """
    Ask the user for a valid menu choice.
    Keeps asking until the user enters a number between 0 and 13.
    """

    while True:
        try:
            choice = int(input(GREEN + "➜ Wähle eine der Optionen (0-13): " + RESET))

            if 0 <= choice <= 13:
                return choice

            print(RED + "Ungültige Eingabe, bitte versuche es erneut." + RESET)

        except ValueError:
            print(RED + "Ungültige Eingabe, bitte gebe eine Zahl zwischen 0 und 13 ein." + RESET)


def exit_program():
    """
    Exit the application.
    Prints the goodbye message and returns False to stop the main loop.
    """

    print("Bye!")
    return False


def navigate_menu(choice, active_user_id, active_user_name):
    """
    Run the selected menu command for the active user.
    """

    if choice == 0:
        return exit_program()

    command_dict = {
        1: list_movies,
        2: add_movie,
        3: delete_movie,
        4: change_movie,
        5: stats,
        6: random_movie,
        7: search_movie,
        8: movie_ranking,
        9: create_rating_histogramm,
        10: movie_ranking_by_year,
        11: filter_movies,
        12: generate_website
    }

    command_function = command_dict[choice]
    command_function(active_user_id, active_user_name)

    return True


def list_movies(active_user_id, active_user_name):
    """
    Print all movies for the active user.
    """

    movies = storage.list_movies(active_user_id)

    print()
    num_items = len(movies)
    print(GREEN + BOLD + f"{active_user_name}: {num_items} Filme insgesamt" + RESET)
    print(GREEN + "────────────────────────────────────" + RESET)

    for title, movie_data in movies.items():
        rating = movie_data["rating"]
        year = movie_data["year"]

        print(f"{title} ({year}): {rating}")


def add_movie(active_user_id, active_user_name):
    """
    Add a new movie to the active user's movie collection.
    """

    movies = storage.list_movies(active_user_id)

    movie_title = get_non_empty_title(
        GREEN + "Welchen Film möchtest du hinzufügen: " + RESET
    )

    # Fetch the movie information from the OMDb API.
    movie_data = movie_fetcher.fetch_movie_data(movie_title)

    # Stop if the movie was not found or the API request failed.
    if movie_data is None:
        print(RED + "Der Film konnte nicht hinzugefügt werden." + RESET)
        return

    if movie_data["title"] in movies:
        print(RED + f'{movie_data["title"]} existiert bereits.' + RESET)
        return

    storage.add_movie(
        active_user_id,
        movie_data["title"],
        movie_data["year"],
        movie_data["rating"],
        movie_data["poster_url"],
        movie_data["imdb_url"],
        movie_data["country"],
        movie_data["flag_url"]
    )

    print(
        GREEN
        + f'{movie_data["title"]} wurde zu {active_user_name}s Sammlung hinzugefügt.'
        + RESET
    )


def delete_movie(active_user_id, active_user_name):
    """
    Delete a movie from the active user's movie collection.
    """

    movies = storage.list_movies(active_user_id)

    movie_title = get_non_empty_title(
        GREEN + "Welchen Film möchtest du entfernen? " + RESET
    )

    if movie_title in movies:
        storage.delete_movie(active_user_id, movie_title)
        print(GREEN + f"{movie_title} wurde gelöscht." + RESET)
    else:
        print(RED + f"Der Film {movie_title} existiert nicht." + RESET)


def change_movie(active_user_id, active_user_name):
    """
    Add or update a note for an existing movie
    in the active user's collection.
    """

    movies = storage.list_movies(active_user_id)

    movie_title = get_non_empty_title(
        GREEN + "Gebe den Filmtitel ein: " + RESET
    )

    if movie_title in movies:
        movie_note = input(GREEN + "Gebe eine Notiz zum Film ein: " + RESET).strip()

        storage.update_movie(active_user_id, movie_title, movie_note)
        print(GREEN + f"{movie_title} wurde aktualisiert." + RESET)
    else:
        print(RED + f"Der Film {movie_title} existiert nicht." + RESET)


def stats(active_user_id, active_user_name):
    """
    Print statistics about the movie ratings.
    Calculates the average rating, median rating, best-rated movie
    and worst-rated movie.
    """

    movies = storage.list_movies(active_user_id)

    if len(movies) == 0:
        print(RED + "Keine Filme in der Datenbank." + RESET)
        return

    ratings = []

    for movie_data in movies.values():
        ratings.append(movie_data["rating"])

    average_rating = sum(ratings) / len(ratings)

    print()
    print(GREEN + BOLD + "Statistiken" + RESET)
    print(GREEN + "────────────────────────────────────" + RESET)
    print(f"Durchschnittliche Bewertung: {average_rating:.1f}")

    ratings.sort()
    amount = len(ratings)
    middle = amount // 2

    if amount % 2 == 1:
        median = ratings[middle]
    else:
        median = (ratings[middle - 1] + ratings[middle]) / 2

    print(f"Der Median beträgt: {median:.1f}")

    highest_rating = max(ratings)
    lowest_rating = min(ratings)

    print()
    print(GREEN + BOLD + "Bester Film:" + RESET)
    for title, movie_data in movies.items():
        if movie_data["rating"] == highest_rating:
            print(f'{title} ({movie_data["year"]}): {movie_data["rating"]}')

    print()
    print(GREEN + BOLD + "Schlechtester Film:" + RESET)
    for title, movie_data in movies.items():
        if movie_data["rating"] == lowest_rating:
            print(f'{title} ({movie_data["year"]}): {movie_data["rating"]}')


def random_movie(active_user_id, active_user_name):
    """
    Print a random movie from the database.
    Selects one movie from the database and displays its title, year and rating.
    """

    movies = storage.list_movies(active_user_id)

    if len(movies) == 0:
        print(RED + "Keine Filme in der Datenbank." + RESET)
        return

    title = random.choice(list(movies.keys()))
    movie_data = movies[title]

    rating = movie_data["rating"]
    year = movie_data["year"]

    print(GREEN + f"Zufälliger Film: {title} ({year}) - {rating}" + RESET)


def search_movie(active_user_id, active_user_name):
    """
    Search for movies by title.
    Rejects empty search input and finds movies by partial title match.
    """

    movies = storage.list_movies(active_user_id)

    search_title = get_non_empty_title(GREEN + "Suche Titel: " + RESET)
    search_title_lower = search_title.lower()

    found = False

    for title, movie_data in movies.items():
        rating = movie_data["rating"]
        year = movie_data["year"]

        if search_title_lower in title.lower():
            print(f"{title} ({year}): {rating}")
            found = True

    if found is False:
        movie_titles = list(movies.keys())

        similar_movies = difflib.get_close_matches(
            search_title,
            movie_titles,
            n=3,
            cutoff=0.4
        )

        if len(similar_movies) > 0:
            print(RED + f'Der Film "{search_title}" existiert nicht.' + RESET)
            print(GREEN + "Meintest du:" + RESET)

            for movie_title in similar_movies:
                print(movie_title)
        else:
            print(RED + f'Der Film "{search_title}" existiert nicht.' + RESET)


def movie_ranking(active_user_id, active_user_name):
    """
    Print movies sorted by rating.
    Creates a sortable list from the movie database and displays
    the movies from highest to lowest rating.
    """

    movies = storage.list_movies(active_user_id)

    if len(movies) == 0:
        print(RED + "Keine Filme in der Datenbank." + RESET)
        return

    rating_list = []

    for title, movie_data in movies.items():
        rating = movie_data["rating"]
        year = movie_data["year"]

        rating_list.append([rating, title, year])

    rating_list.sort(reverse=True)

    print()
    print(GREEN + BOLD + "Filme nach Bewertung:" + RESET)

    for item in rating_list:
        rating = item[0]
        title = item[1]
        year = item[2]

        print(f"{title} ({year}), {rating}")


def create_rating_histogramm(active_user_id, active_user_name):
    """
    Create a histogram of movie ratings.
    Collects all ratings from the movie database and saves
    the histogram as a PNG file.
    """

    movies = storage.list_movies(active_user_id)

    if len(movies) == 0:
        print(RED + "Keine Filme in der Datenbank." + RESET)
        return

    filename = get_non_empty_filename()

    if not filename.endswith(".png"):
        filename = filename + ".png"

    ratings = []

    for movie_data in movies.values():
        ratings.append(movie_data["rating"])

    plt.hist(ratings, bins=range(0, 12))
    plt.title("Verteilung der Filmbewertungen")
    plt.xlabel("Bewertung")
    plt.ylabel("Anzahl Filme")
    plt.xticks(range(0, 11))

    plt.savefig(filename)
    plt.close()

    print(GREEN + f"Histogramm wurde als {filename} gespeichert." + RESET)


def movie_ranking_by_year(active_user_id, active_user_name):
    """
    Print movies sorted by release year.
    Asks the user whether the newest movies should be shown first
    or last, then displays all movies with title, year and rating.
    """

    movies = storage.list_movies(active_user_id)

    if len(movies) == 0:
        print(RED + "Keine Filme in der Datenbank." + RESET)
        return

    while True:
        sort_choice = input(
            GREEN + "Neueste Filme zuerst anzeigen? (y/n): " + RESET
        ).lower().strip()

        if sort_choice == "y":
            newest_first = True
            break

        if sort_choice == "n":
            newest_first = False
            break

        print(RED + "Bitte gib y oder n ein." + RESET)

    year_list = []

    for title, movie_data in movies.items():
        year = movie_data["year"]
        rating = movie_data["rating"]

        year_list.append([year, title, rating])

    year_list.sort(reverse=newest_first)

    print()
    print(GREEN + BOLD + "Filme nach Erscheinungsjahr:" + RESET)

    for item in year_list:
        year = item[0]
        title = item[1]
        rating = item[2]

        print(f"{title} ({year}): {rating}")


def filter_movies(active_user_id, active_user_name):
    """
    Filter movies by minimum rating, start year and end year.
    Empty input means that the related filter should not be used.
    Invalid numeric input asks the user to try again.
    """

    movies = storage.list_movies(active_user_id)

    min_rating = get_optional_float(
        GREEN + "Enter minimum rating (leave blank for no minimum rating): " + RESET
    )

    start_year = get_optional_int(
        GREEN + "Enter start year (leave blank for no start year): " + RESET
    )

    end_year = get_optional_int(
        GREEN + "Enter end year (leave blank for no end year): " + RESET
    )

    print()
    print(GREEN + BOLD + "Filtered Movies:" + RESET)

    found = False

    for title, movie_data in movies.items():
        rating = movie_data["rating"]
        year = movie_data["year"]

        if min_rating is not None and rating < min_rating:
            continue

        if start_year is not None and year < start_year:
            continue

        if end_year is not None and year > end_year:
            continue

        print(f"{title} ({year}): {rating}")
        found = True

    if found is False:
        print(RED + "Keine passenden Filme gefunden." + RESET)


def serialize_movie(title, movie_data):
    """
    Convert one movie into an HTML list item.
    """

    poster_url = movie_data["poster_url"]
    year = movie_data["year"]
    rating = movie_data["rating"]
    note = movie_data["note"]
    imdb_url = movie_data["imdb_url"]
    country = movie_data["country"]
    flag_url = movie_data["flag_url"]

    # Use a local fallback image if the API does not provide a poster.
    if poster_url is None or poster_url == "" or poster_url == "N/A":
        poster_url = FALLBACK_POSTER

    if note is None:
        note = ""

    if country is None:
        country = ""

    if flag_url is None:
        flag_url = ""

    # Escape text before writing it into HTML.
    safe_title = html.escape(title)
    safe_note = html.escape(note, quote=True)
    safe_country = html.escape(country)
    safe_title_attribute = html.escape(title.lower(), quote=True)
    safe_country_attribute = html.escape(country.lower(), quote=True)

    output = ""
    output += (
        f'        <li data-title="{safe_title_attribute}" '
        f'data-year="{year}" '
        f'data-rating="{rating}" '
        f'data-country="{safe_country_attribute}" '
        f'data-country-label="{safe_country}">\n'
    )
    output += '            <div class="movie">\n'
    output += f'                <a href="{imdb_url}" target="_blank">\n'
    output += (
        f'                    <img class="movie-poster" '
        f'src="{poster_url}" '
        f'title="{safe_note}"/>\n'
    )
    output += "                </a>\n"
    output += f'                <div class="movie-title">{safe_title}</div>\n'
    output += f'                <div class="movie-year">{year}</div>\n'
    output += f'                <div class="movie-rating">Rating: {rating}</div>\n'

    if flag_url != "":
        output += (
            f'                <div class="movie-country">'
            f'<img class="movie-flag" src="{flag_url}" alt="{safe_country} flag"/> '
            f'<span class="movie-country-name">{safe_country}</span></div>\n'
        )
    else:
        output += (
            f'                <div class="movie-country">'
            f'<span class="movie-country-name">{safe_country}</span></div>\n'
        )

    output += "            </div>\n"
    output += "        </li>\n"

    return output


def generate_website(active_user_id, active_user_name):
    """
    Generate an HTML website from the active user's movie collection.
    """

    movies = storage.list_movies(active_user_id)

    movie_grid = ""

    # Create one HTML block for every movie.
    for title, movie_data in movies.items():
        movie_grid += serialize_movie(title, movie_data)

    # Read the HTML template.
    with open("index_template.html", "r", encoding="utf-8") as template_file:
        template = template_file.read()

    # Replace the placeholders with the user-specific app title and movie grid.
    safe_user_name = html.escape(active_user_name)
    movie_count = len(movies)

    html_output = template.replace(
        "__TEMPLATE_TITLE__",
        f"&#127916; {safe_user_name}'s Movie Vault"
    )

    html_output = html_output.replace(
        "__TEMPLATE_SUBTITLE__",
        f"{movie_count} movies &middot; Personal collection"
    )

    html_output = html_output.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    # Write the final website.
    with open("index.html", "w", encoding="utf-8") as output_file:
        output_file.write(html_output)

    print("Website was generated successfully.")


def normalize_user_name(user_name):
    """
    Clean up a user name before saving or searching it.
    Example: "  sara   müller  " becomes "Sara Müller".
    """

    # Remove spaces at the beginning and end.
    cleaned_name = user_name.strip()

    # Replace multiple spaces inside the name with one single space.
    cleaned_name = " ".join(cleaned_name.split())

    # Convert the name into a consistent format.
    cleaned_name = cleaned_name.title()

    return cleaned_name


def get_non_empty_title(prompt):
    """
    Ask the user for a movie title and reject empty input.
    """

    while True:
        title = input(prompt).strip()

        if title != "":
            return title

        print(RED + "Der Filmtitel darf nicht leer sein." + RESET)


def get_rating():
    """
    Ask the user for a valid rating between 0 and 10.
    """

    while True:
        try:
            rating = float(input(GREEN + "Bewertung des Films (0-10): " + RESET))

            if 0 <= rating <= 10:
                return rating

            print(RED + "Die Bewertung muss zwischen 0 und 10 liegen." + RESET)

        except ValueError:
            print(RED + "Bitte gib eine gültige Zahl ein." + RESET)


def get_year():
    """
    Ask the user for a valid release year.
    """

    while True:
        try:
            year = int(input(GREEN + "Erscheinungsjahr: " + RESET))

            if 1900 <= year <= 2100:
                return year

            print(RED + "Bitte gib ein realistisches Jahr ein." + RESET)

        except ValueError:
            print(RED + "Bitte gib eine gültige Jahreszahl ein." + RESET)


def get_non_empty_filename():
    """
    Ask the user for a non-empty filename.
    """

    while True:
        filename = input(
            GREEN + "Tippe einen Dateinamen für das Histogramm ein: " + RESET
        ).strip()

        if filename != "":
            return filename

        print(RED + "Der Dateiname darf nicht leer sein." + RESET)


def get_optional_float(prompt):
    """
    Ask for an optional float value.
    Empty input returns None. Invalid input asks again.
    """

    while True:
        user_value = input(prompt).strip()

        if user_value == "":
            return None

        try:
            return float(user_value)

        except ValueError:
            print(RED + "Bitte gib eine gültige Zahl ein oder lasse das Feld leer." + RESET)


def get_optional_int(prompt):
    """
    Ask for an optional integer value.
    Empty input returns None. Invalid input asks again.
    """

    while True:
        user_value = input(prompt).strip()

        if user_value == "":
            return None

        try:
            return int(user_value)

        except ValueError:
            print(RED + "Bitte gib eine gültige Jahreszahl ein oder lasse das Feld leer." + RESET)


if __name__ == "__main__":
    main()