from imdbinfo import get_movie
import json

movie = get_movie("27331527", "en")

with open("movie.json", "w", encoding="utf-8") as f:
    json.dump(movie.model_dump(), f, indent=2, ensure_ascii=False, default=str)

print("Saved to movie.json")