const movieGrid = document.querySelector(".movie-grid");
const movieItems = Array.from(movieGrid.querySelectorAll("li"));

const searchInput = document.getElementById("movie-search");
const countryFilter = document.getElementById("country-filter");
const sortSelect = document.getElementById("sort-select");

movieItems.forEach((movieItem, index) => {
  movieItem.dataset.index = String(index);
});

function fillCountryFilter() {
  const countries = new Map();

  movieItems.forEach((movieItem) => {
    const countryValue = movieItem.dataset.country;
    const countryLabel = movieItem.dataset.countryLabel;

    if (countryValue !== "") {
      countries.set(countryValue, countryLabel);
    }
  });

  const sortedCountries = Array.from(countries.entries()).sort();

  sortedCountries.forEach(([countryValue, countryLabel]) => {
    const option = document.createElement("option");
    option.value = countryValue;
    option.textContent = countryLabel;
    countryFilter.appendChild(option);
  });
}

function updateMovies() {
  const searchText = searchInput.value.toLowerCase().trim();
  const selectedCountry = countryFilter.value;
  const sortValue = sortSelect.value;

  movieItems.forEach((movieItem) => {
    const title = movieItem.dataset.title;
    const country = movieItem.dataset.country;

    const matchesSearch = title.includes(searchText);
    const matchesCountry = selectedCountry === "all" || country === selectedCountry;

    if (matchesSearch && matchesCountry) {
      movieItem.style.display = "";
    } else {
      movieItem.style.display = "none";
    }
  });

  const sortedMovies = [...movieItems].sort((firstMovie, secondMovie) => {
    if (sortValue === "title") {
      return firstMovie.dataset.title.localeCompare(secondMovie.dataset.title);
    }

    if (sortValue === "year-desc") {
      return Number(secondMovie.dataset.year) - Number(firstMovie.dataset.year);
    }

    if (sortValue === "year-asc") {
      return Number(firstMovie.dataset.year) - Number(secondMovie.dataset.year);
    }

    if (sortValue === "rating-desc") {
      return Number(secondMovie.dataset.rating) - Number(firstMovie.dataset.rating);
    }

    if (sortValue === "rating-asc") {
      return Number(firstMovie.dataset.rating) - Number(secondMovie.dataset.rating);
    }

    return Number(firstMovie.dataset.index) - Number(secondMovie.dataset.index);
  });

  sortedMovies.forEach((movieItem) => {
    movieGrid.appendChild(movieItem);
  });
}

fillCountryFilter();

searchInput.addEventListener("input", updateMovies);
countryFilter.addEventListener("change", updateMovies);
sortSelect.addEventListener("change", updateMovies);