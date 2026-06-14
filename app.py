import streamlit as st
import pandas as pd
from imdbinfo import get_movie

st.title("IMDb Poster Fetcher")

st.info("""
**Notes:**
- Global Tent IDs and IMDb IDs must have the same count.
- The order matters.
- The first Global Tent ID is matched with the first IMDb ID, the second with the second, and so on.
""")

global_tent_ids_text = st.text_area(
    "Global Tent IDs (separated by commas):",
    placeholder="123456,456123,456789"
)

imdb_ids_text = st.text_area(
    "IMDb IDs (separated by commas):",
    placeholder="tt0111161,tt0133093,tt32477632"
)

if st.button("Run"):
    global_tent_ids = [x.strip() for x in global_tent_ids_text.split(",") if x.strip()]
    imdb_ids = [x.strip() for x in imdb_ids_text.split(",") if x.strip()]

    if len(global_tent_ids) != len(imdb_ids):
        st.error(f"Count mismatch: {len(global_tent_ids)} global_tent_ids vs {len(imdb_ids)} imdb_ids")
    else:
        results = []
        errors = []

        progress = st.progress(0)
        status = st.empty()

        total_rows = len(imdb_ids)

        for index, (global_tent_id, imdb_id) in enumerate(zip(global_tent_ids, imdb_ids), start=1):
            percent = round((index / total_rows) * 100, 1)

            try:
                movie = get_movie(imdb_id)

                if not movie.cover_url:
                    errors.append({
                        "global_tent_id": global_tent_id,
                        "imdb_id": imdb_id,
                        "error": "No poster found"
                    })

                    status.write(f"[{index}/{total_rows}] ({percent}%) NO POSTER: {imdb_id}")
                    progress.progress(index / total_rows)
                    continue

                results.append({
                    "tent_id": "",
                    "global_tent_id": global_tent_id,
                    "url": movie.cover_url
                })

                status.write(f"[{index}/{total_rows}] ({percent}%) OK: {imdb_id}")

            except Exception as e:
                errors.append({
                    "global_tent_id": global_tent_id,
                    "imdb_id": imdb_id,
                    "error": str(e)
                })

                status.write(f"[{index}/{total_rows}] ({percent}%) ERROR: {imdb_id} - {e}")

            progress.progress(index / total_rows)

        result_df = pd.DataFrame(results)
        error_df = pd.DataFrame(errors)

        st.success(f"Done! Success: {len(results)} | Failed: {len(errors)} | Total: {total_rows}")

        st.subheader("Results")
        st.dataframe(result_df)

        st.download_button(
            "Download output.csv",
            result_df.to_csv(index=False),
            "output.csv",
            "text/csv"
        )

        if errors:
            st.subheader("Errors")
            st.dataframe(error_df)

            st.download_button(
                "Download errors.csv",
                error_df.to_csv(index=False),
                "errors.csv",
                "text/csv"
            )