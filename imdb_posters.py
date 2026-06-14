from imdbinfo import get_movie
import csv

results = []
errors = []

# Broj redova (minus header)
with open("input.csv", encoding="utf-8") as f:
    total_rows = sum(1 for _ in f) - 1

with open("input.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for index, row in enumerate(reader, start=1):
        global_tent_id = row["global_tent_id"]
        imdb_id = row["imdb_id"]

        percent = round((index / total_rows) * 100, 1)

        try:
            movie = get_movie(imdb_id)

            results.append([
                global_tent_id,
                imdb_id,
                movie.title,
                movie.cover_url
            ])

            print(f"[{index}/{total_rows}] ({percent}%) OK: {imdb_id}")

        except Exception as e:
            errors.append([
                global_tent_id,
                imdb_id,
                str(e)
            ])

            print(f"[{index}/{total_rows}] ({percent}%) ERROR: {imdb_id} - {e}")

# Glavni output
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "global_tent_id",
        "imdb_id",
        "title",
        "poster"
    ])

    writer.writerows(results)

# Error output
if errors:
    with open("errors.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "global_tent_id",
            "imdb_id",
            "error"
        ])

        writer.writerows(errors)

success_count = len(results)
failed_count = len(errors)

print("\n==============================")
print("Images gathered!")
print("==============================")
print(f"Success: {success_count}")
print(f"Failed: {failed_count}")
print(f"Total: {total_rows}")
print("==============================")