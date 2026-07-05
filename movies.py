import random
import difflib
import movie_fetcher

import matplotlib.pyplot as plt
import pyfiglet

import movie_storage_sql as storage


# Terminal colors
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"


def main():
    """
    Start the movie database application.
    Movie data is loaded from and saved to a SQLite database
    through the storage module.
    """

    while True:
        show_menu()
        choice = user_input()
        keep_running = navigate_menu(choice)

        if keep_running is False:
            break

        input(GREEN + "\nDrücke Enter, um zum Menü zurückzukehren..." + RESET)


def show_menu():
    """
    Display the main menu.
    Shows all available menu options to the user, including the exit option.
    """

    print()

    title = pyfiglet.figlet_format("Movie DB", font="slant")
    print(GREEN + BOLD + title + RESET)
    print(GREEN + "╔════════════════════════════════════╗" + RESET)
    print(GREEN + "║                MENÜ                ║" + RESET)
    print(GREEN + "╠════════════════════════════════════╣" + RESET)
    print(GREEN + "║ 0. Exit                            ║" + RESET)
    print(GREEN + "║ 1. Alle Filme anzeigen             ║" + RESET)
    print(GREEN + "║ 2. Neuen Film hinzufügen           ║" + RESET)
    print(GREEN + "║ 3. Film aus DB entfernen           ║" + RESET)
    print(GREEN + "║ 4. Filmbewertung anpassen          ║" + RESET)
    print(GREEN + "║ 5. Stats                           ║" + RESET)
    print(GREEN + "║ 6. Zufälliger Film                 ║" + RESET)
    print(GREEN + "║ 7. Filmsuche                       ║" + RESET)
    print(GREEN + "║ 8. Filme nach Bewertung            ║" + RESET)
    print(GREEN + "║ 9. Bewertungs-Histogramm erstellen ║" + RESET)
    print(GREEN + "║ 10. Filme nach Jahr sortieren.     ║" + RESET)
    print(GREEN + "║ 11. Filme filtern                  ║" + RESET)
    print(GREEN + "║ 12. Website generieren             ║" + RESET)
    print(GREEN + "╚════════════════════════════════════╝" + RESET)
    print()


def user_input():
    """
    Ask the user for a valid menu choice.
    Keeps asking until the user enters a number between 0 and 11.
    """

    while True:
        try:
            choice = int(input(GREEN + "➜ Wähle eine der Optionen (0-12): " + RESET))

            if 0 <= choice <= 12:
                return choice

            print(RED + "Ungültige Eingabe, bitte versuche es erneut." + RESET)

        except ValueError:
            print(RED + "Ungültige Eingabe, bitte gebe eine Zahl zwischen 0 und 12 ein." + RESET)


def exit_program():
    """
    Exit the application.
    Prints the goodbye message and returns False to stop the main loop.
    """

    print("Bye!")
    return False


def navigate_menu(choice):
    """
    Run the selected menu command.
    Uses a dispatch dictionary to connect the user's menu choice
    with the matching function.
    """

    command_dict = {
        0: exit_program,
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
    result = command_function()

    if result is False:
        return False

    return True


def list_movies():
    """
    Print all movies in the database.
    Shows each movie with its title, release year and rating.
    """

    movies = storage.list_movies()

    print()
    num_items = len(movies)
    print(GREEN + BOLD + f"{num_items} Filme insgesamt" + RESET)
    print(GREEN + "────────────────────────────────────" + RESET)

    for title, movie_data in movies.items():
        rating = movie_data["rating"]
        year = movie_data["year"]

        print(f"{title} ({year}): {rating}")


def add_movie():
    """
    Add a new movie to the database.
    Asks the user for a title, fetches movie data from the OMDb API,
    and stores the movie in the SQLite database.
    """

    movies = storage.list_movies()

    movie_title = get_non_empty_title(
        GREEN + "Welchen Film möchtest du hinzufügen: " + RESET
    )

    if movie_title in movies:
        print(RED + f"{movie_title} existiert bereits." + RESET)
        return

    # Fetch the movie information from the OMDb API.
    movie_data = movie_fetcher.fetch_movie_data(movie_title)

    # Stop if the movie was not found or the API request failed.
    if movie_data is None:
        print(RED + "Der Film konnte nicht hinzugefügt werden." + RESET)
        return

    storage.add_movie(
        movie_data["title"],
        movie_data["year"],
        movie_data["rating"],
        movie_data["poster_url"]
    )

    print(GREEN + f'{movie_data["title"]} erfolgreich hinzugefügt' + RESET)


def delete_movie():
    """
    Delete a movie from the database.
    Asks for a non-empty title and deletes the movie if it exists.
    """

    movies = storage.list_movies()

    movie_title = get_non_empty_title(
        GREEN + "Welchen Film möchtest du entfernen? " + RESET
    )

    if movie_title in movies:
        storage.delete_movie(movie_title)
        print(GREEN + f"{movie_title} wurde gelöscht." + RESET)
    else:
        print(RED + f"Der Film {movie_title} existiert nicht." + RESET)


def change_movie():
    """
    Update the rating of an existing movie.
    Asks for a non-empty title and a valid rating, then updates the movie.
    """

    movies = storage.list_movies()

    movie_title = get_non_empty_title(
        GREEN + "Gebe den Filmtitel ein: " + RESET
    )

    if movie_title in movies:
        new_rating = get_rating()
        storage.update_movie(movie_title, new_rating)
        print(GREEN + f"{movie_title} wurde aktualisiert" + RESET)
    else:
        print(RED + f"Der Film {movie_title} existiert nicht." + RESET)


def stats():
    """
    Print statistics about the movie ratings.
    Calculates the average rating, median rating, best-rated movie
    and worst-rated movie.
    """

    movies = storage.list_movies()

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


def random_movie():
    """
    Print a random movie from the database.
    Selects one movie from the database and displays its title, year and rating.
    """

    movies = storage.list_movies()

    if len(movies) == 0:
        print(RED + "Keine Filme in der Datenbank." + RESET)
        return

    title = random.choice(list(movies.keys()))
    movie_data = movies[title]

    rating = movie_data["rating"]
    year = movie_data["year"]

    print(GREEN + f"Zufälliger Film: {title} ({year}) - {rating}" + RESET)


def search_movie():
    """
    Search for movies by title.
    Rejects empty search input and finds movies by partial title match.
    """

    movies = storage.list_movies()

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


def movie_ranking():
    """
    Print movies sorted by rating.
    Creates a sortable list from the movie database and displays
    the movies from highest to lowest rating.
    """

    movies = storage.list_movies()

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


def create_rating_histogramm():
    """
    Create a histogram of movie ratings.
    Collects all ratings from the movie database and saves
    the histogram as a PNG file.
    """

    movies = storage.list_movies()

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


def movie_ranking_by_year():
    """
    Print movies sorted by release year.
    Asks the user whether the newest movies should be shown first
    or last, then displays all movies with title, year and rating.
    """

    movies = storage.list_movies()

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


def filter_movies():
    """
    Filter movies by minimum rating, start year and end year.
    Empty input means that the related filter should not be used.
    Invalid numeric input asks the user to try again.
    """

    movies = storage.list_movies()

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

    output = ""
    output += "        <li>\n"
    output += '            <div class="movie">\n'
    output += (
        f'                <img class="movie-poster" '
        f'src="{poster_url}"/>\n'
    )
    output += f'                <div class="movie-title">{title}</div>\n'
    output += f'                <div class="movie-year">{year}</div>\n'
    output += "            </div>\n"
    output += "        </li>\n"

    return output


def generate_website():
    """
    Generate an HTML website from the movies in the database.
    """

    movies = storage.list_movies()

    print(f"Generating website for {len(movies)} movies.")
    print(movies)

    movie_grid = ""

    # Create one HTML block for every movie.
    for title, movie_data in movies.items():
        movie_grid += serialize_movie(title, movie_data)

    # Read the HTML template.
    with open("index_template.html", "r", encoding="utf-8") as template_file:
        template = template_file.read()

    # Replace the placeholders with the app title and movie grid.
    html_output = template.replace("__TEMPLATE_TITLE__", "My Movie App")
    html_output = html_output.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    # Write the final website.
    with open("index.html", "w", encoding="utf-8") as output_file:
        output_file.write(html_output)

    print("Website was generated successfully.")


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