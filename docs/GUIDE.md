# TP — Build a Python/Pandas Pipeline for Public Data (Movies edition)

**Goal:** practice fetching public data from an API, cleaning it with pandas,
and exporting it into a clean, reusable folder structure — this time using
**movie data** (TMDb API) instead of the French communes example.

**Level:** beginner/intermediate. Each step gives you the goal, hints, and a
code skeleton with `TODO`s — not a full solution. Try to fill it in yourself
before peeking at the hints.

**Tools:** Python 3.10+, VS Code, Git/GitHub.

---

## 0. Setup

### 0.1 Get a free TMDb API key

TMDb (The Movie Database) has a free, well-documented API, but it requires
a key (unlike the French communes API).

1. Create a free account at https://www.themoviedb.org/
2. Go to **Settings → API** and request a free "Developer" API key.
3. You'll get an **API Read Access Token** (a long string) — keep it secret,
   never commit it to GitHub.

### 0.2 Create the GitHub repo

```bash
git clone https://github.com/<your-username>/movies-data-pipeline.git
cd movies-data-pipeline
code .
```

### 0.3 Project skeleton

```
movies-data-pipeline/
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
├── src/
│   ├── __init__.py
│   ├── download.py
│   ├── clean.py
│   └── split.py
├── scripts/
│   ├── 01_download.py
│   ├── 02_clean.py
│   └── 03_split.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### 0.4 Virtual environment + dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

`requirements.txt`:
```
requests
pandas
pyarrow
python-dotenv
```

```bash
pip install -r requirements.txt
```

### 0.5 Store the API key safely

`.env`:
```
TMDB_API_KEY=your_token_here
```

`.gitignore` — add **at least**:
```
venv/
__pycache__/
.env
data/raw/
data/processed/
```

> The `.env` file must never be committed. This is the standard way to keep
> secrets out of GitHub.

### ✅ Checkpoint 0
- `git status` is clean, `venv` activated, `.env` is in `.gitignore` (check
  with `git check-ignore -v .env`).

---

## 1. Choose your dataset scope

TMDb has many endpoints. To keep this TP simple, we'll build a dataset of
**popular movies**, endpoint:

```
GET https://api.themoviedb.org/3/movie/popular?language=en-US&page=1
```

It's **paginated** (20 movies per page). We'll fetch several pages to get
a few hundred movies — good practice for pagination, which you'll meet
in almost every real-world API.

Fields we care about: `id`, `title`, `release_date`, `genre_ids`,
`vote_average`, `vote_count`, `popularity`, `original_language`.

### ✅ Checkpoint 1
- You tested the endpoint once in your browser or with `curl`
  (add the header `Authorization: Bearer <token>`) and saw JSON back.

---

## 2. Step 1 — Download the raw data (`src/download.py`)

**Goal:** fetch several pages of popular movies and save the raw,
unmodified response to `data/raw/`.

### Skeleton — `src/download.py`

```python
import json
import time
from pathlib import Path
import requests

API_URL = "https://api.themoviedb.org/3/movie/popular"
RAW_PATH = Path("data/raw/movies_raw.json")


def fetch_page(page: int, api_key: str, max_retries: int = 3) -> dict:
    """Fetch one page of popular movies. Retries on failure."""
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"language": "en-US", "page": page}

    for attempt in range(1, max_retries + 1):
        try:
            # TODO: call requests.get(API_URL, headers=headers, params=params, timeout=30)
            # TODO: raise an error if the status code isn't 200
            #       (hint: response.raise_for_status())
            # TODO: return response.json()
            pass
        except requests.RequestException as e:
            print(f"Page {page}, attempt {attempt} failed: {e}")
            # TODO: time.sleep(2 * attempt)
    raise RuntimeError(f"Failed to fetch page {page} after retries")


def fetch_all_pages(api_key: str, n_pages: int = 10) -> list:
    """Fetch n_pages of popular movies and concatenate the results."""
    all_movies = []
    for page in range(1, n_pages + 1):
        # TODO: call fetch_page(page, api_key)
        # TODO: extract the "results" list from the response
        # TODO: extend all_movies with it
        # TODO: be polite to the API: time.sleep(0.25) between calls
        pass
    return all_movies


def save_raw(data: list, path: Path = RAW_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # TODO: write `data` to `path` as JSON, ensure_ascii=False
```

### Skeleton — `scripts/01_download.py`

```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
import os
from src.download import fetch_all_pages, save_raw

load_dotenv()
api_key = os.environ["TMDB_API_KEY"]

movies = fetch_all_pages(api_key, n_pages=10)
save_raw(movies)
print(f"Saved {len(movies)} movies.")
```

### Hints
- `timeout=30` avoids hanging forever.
- The raw file should stay untouched afterwards — if cleaning goes wrong,
  you fix `clean.py` and re-run, not re-download.
- A small `time.sleep(0.25)` between page requests avoids hitting TMDb's
  rate limit.

### ✅ Checkpoint 2
- `python scripts/01_download.py` creates `data/raw/movies_raw.json` with
  ~200 movies (10 pages × 20).

---

## 3. Step 2 — Clean the data (`src/clean.py`)

Typical problems you'll meet with this dataset:

| Problem | What to do |
|---|---|
| `genre_ids` is a list of numbers (`[28, 12]`), not readable genre names | Map ids → names using TMDb's genre list, or just flatten to a string for now |
| `release_date` is a string, sometimes empty | Convert with `pd.to_datetime(..., errors="coerce")` |
| `vote_average` / `popularity` should be numeric | `pd.to_numeric(..., errors="coerce")` |
| Duplicate movies (same movie can appear across pages if the list shifts) | `df.drop_duplicates(subset="id")` |
| Missing `release_date` → can't extract a year | Keep it as `NaT`, don't crash on it |

### Skeleton — `src/clean.py`

```python
import pandas as pd

KEEP_COLS = ["id", "title", "release_date", "genre_ids",
             "original_language", "vote_average", "vote_count", "popularity"]


def load_raw(path: str) -> pd.DataFrame:
    # TODO: read the JSON file into a DataFrame
    ...


def clean_movies(df: pd.DataFrame) -> pd.DataFrame:
    df = df[KEEP_COLS].copy()

    # TODO 1: convert "release_date" to datetime with errors="coerce"

    # TODO 2: create a "release_year" column (Int64, nullable) from release_date
    #         hint: df["release_date"].dt.year, then cast to "Int64"

    # TODO 3: convert "vote_average", "vote_count", "popularity" to numeric

    # TODO 4: flatten "genre_ids" (a list) into a comma-separated string,
    #         e.g. [28, 12] -> "28,12"

    # TODO 5: drop duplicates on "id"

    # TODO 6: sort by "popularity" descending

    return df


def save_clean(df: pd.DataFrame, csv_path: str, parquet_path: str) -> None:
    # TODO: save to both CSV and Parquet
    ...
```

### Skeleton — `scripts/02_clean.py`

```python
from src.clean import load_raw, clean_movies, save_clean

df = load_raw("data/raw/movies_raw.json")
df_clean = clean_movies(df)
save_clean(df_clean, "data/processed/movies_clean.csv",
                       "data/processed/movies_clean.parquet")
print(df_clean.shape)
print(df_clean.dtypes)
```

### Hints
- `pd.to_datetime(df["release_date"], errors="coerce")` turns bad/empty
  dates into `NaT` instead of crashing.
- Getting `ValueError: Cannot convert non-finite values`? You tried
  `.astype("Int64")` before removing `NaN`s with `errors="coerce"` — always
  coerce first.
- (Bonus, optional) TMDb also exposes `GET /genre/movie/list` — you could
  fetch it once and map `genre_ids` to real names like `"Action, Adventure"`
  instead of raw numbers.

### ✅ Checkpoint 3
- `data/processed/movies_clean.csv` and `.parquet` exist.
- `df["id"].is_unique` is `True`.
- `df["release_year"]` contains plausible years (not garbage).

---

## 4. Step 3 — Split into per-group files (`src/split.py`)

**Goal:** one output file per release year (or per original language),
each with the same columns as the full file.

### Skeleton — `src/split.py`

```python
from pathlib import Path
import pandas as pd


def split_by_group(df: pd.DataFrame, group_col: str, out_dir: str) -> None:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    # TODO: loop over df.groupby(group_col) (drop NaN groups if any),
    #       and for each group write a CSV named after the group value,
    #       e.g. "2023.csv"
```

### Skeleton — `scripts/03_split.py`

```python
import pandas as pd
from src.split import split_by_group

df = pd.read_csv("data/processed/movies_clean.csv")
split_by_group(df, "release_year", "data/final/by_year")
```

### ✅ Checkpoint 4
- `data/final/by_year/` contains one CSV per year (e.g. `2023.csv`,
  `2022.csv`...), and the total row count across all files equals the row
  count of `movies_clean.csv`.

---

## 5. (Bonus) Step 4 — Basic statistics per group

```python
stats = df.groupby("release_year").agg(
    nb_movies=("id", "count"),
    avg_rating=("vote_average", "mean"),
    avg_popularity=("popularity", "mean"),
)
```

Try also: top 10 movies by `popularity`, or average rating by
`original_language`.

---

## 6. Final verification script

Write a small `scripts/04_check.py` that:

1. Loads `movies_clean.csv` and checks the row count is roughly what you
   expect (~200 if you fetched 10 pages).
2. Asserts `df["id"].is_unique`.
3. Prints the sorted list of unique `release_year` values to spot anything
   odd (e.g. a year of `9999` or `NaN` galore).
4. Loads the `.parquet` version and checks it has the same shape as the CSV.
5. Sums the row counts of every file in `data/final/by_year/*.csv` and
   asserts it equals the total.

---

## 7. Common errors cheat-sheet

| Error | Likely cause | Fix |
|---|---|---|
| `401 Unauthorized` | Wrong/missing API key or bad header | Check `Authorization: Bearer <token>`, and that `.env` is loaded |
| `429 Too Many Requests` | Fetching pages too fast | Add `time.sleep(...)` between calls |
| `ValueError: Cannot convert non-finite values` | `.astype("Int64")` on unclean data | `pd.to_numeric(..., errors="coerce")` first |
| `release_year` full of `NaN` | `release_date` wasn't parsed as datetime first | Convert with `pd.to_datetime(..., errors="coerce")` before `.dt.year` |
| `ModuleNotFoundError: No module named 'src'` | script run from wrong folder | keep the `sys.path.append(...)` line shown above |
| Secret key ends up on GitHub | `.env` wasn't in `.gitignore` in time | Remove it from history (`git rm --cached .env`), rotate the key on TMDb |

---

## 8. Wrap-up on GitHub

```bash
git add .
git commit -m "Pandas pipeline: download, clean, split TMDb popular movies"
git push
```

Double-check `.env` never appears in `git log --all -- .env`. Add a short
`README.md`: data source, how to run the three scripts in order, and what
`TMDB_API_KEY` needs to be set to before running them.

---

## 9. Going further (optional, once this works)

- Map `genre_ids` to real genre names via `GET /genre/movie/list`.
- Fetch more pages, or switch endpoint to `top_rated` or `now_playing`
  and compare distributions.
- Add a couple of `pytest` tests for `clean_movies` (e.g. a bad
  `release_date` doesn't crash the pipeline).
- Parameterize `scripts/03_split.py` with `argparse` to choose the group
  column (`release_year` vs `original_language`).
- Try `duckdb.sql("SELECT * FROM 'data/processed/*.parquet' WHERE release_year = 2023")`.