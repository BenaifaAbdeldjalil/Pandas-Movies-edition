# TP — Build a Python/Pandas Pipeline for Public Data (Studio Ghibli edition)

**Goal:** practice fetching public data from an API, cleaning it with pandas,
and exporting it into a clean, reusable folder structure — using the
**Studio Ghibli API**, which needs **no API key at all**.

**Level:** beginner/intermediate. Each step gives you the goal, hints, and a
code skeleton with `TODO`s — not a full solution. Try to fill it in yourself
before peeking at the hints.

**Tools:** Python 3.10+, VS Code, Git/GitHub.

**API used:** https://ghibli-api.vercel.app/api/films — no auth, no sign-up,
returns all 22 Studio Ghibli films as JSON in one single request.

---

## 0. Setup

### 0.1 Create the GitHub repo

```bash
git clone https://github.com/<your-username>/ghibli-data-pipeline.git
cd ghibli-data-pipeline
code .
```

### 0.2 Project skeleton

```
ghibli-data-pipeline/
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
├── .gitignore
└── README.md
```

### 0.3 Virtual environment + dependencies

```bash
python -m venv venv
.\venv\Scripts\activate       # Windows: venv\Scripts\activate
```
project_structure_create.py


`requirements.txt`:
```
requests
pandas
pyarrow
```

echo requests >> requirements.txt
pandas >> requirements.txt  
pyarrow   python-dotenv >> requirements.txt


```bash
pip install -r requirements.txt 
or 
.\venv\Scripts\python.exe -m pip install requests
```

verification :
.\venv\Scripts\python.exe -m pip list 
Package            Version
------------------ ---------
certifi            2026.7.22
charset-normalizer 3.5.1
idna               3.20
pip                26.1.2
requests           2.34.2
urllib3            2.8.0


### 0.4 `.gitignore`

```
venv/
__pycache__/
data/raw/
data/processed/
```

No `.env` needed this time — no secret to hide.

### ✅ Checkpoint 0
- `git status` is clean, `venv` activated, `pandas`/`requests`/`pyarrow`
  installed.

---

## 1. Inspect the API

Open this URL in your browser (or `curl` it) to see the raw shape of the
data before writing any code:

```
https://ghibli-api.vercel.app/api/films
```

You'll get a JSON object with a `"data"` key containing a **list of 22
films**, each with fields like:

```json
{
  "id": "58611129-2dbc-4a81-a72f-77ddfc1b1b49",
  "title": "My Neighbor Totoro",
  "original_title": "となりのトトロ",
  "director": "Hayao Miyazaki",
  "producer": "Hayao Miyazaki",
  "release_date": "1988",
  "running_time": "86",
  "rt_score": "93",
  "people": ["https://ghibli-api.vercel.app/api/people/..."],
  "species": [...],
  "locations": [...],
  "vehicles": [...]
}
```

Notice: `release_date`, `running_time` and `rt_score` are all **strings**,
even though they're numbers — a very common API quirk you'll need to fix.

### ✅ Checkpoint 1
- You've seen the real JSON and identified which fields you want to keep.

---

## 2. Step 1 — Download the raw data (`src/download.py`)

**Goal:** call the API once, and save the **raw, unmodified** response to
`data/raw/`. No pagination, no headers, no key — the simplest possible
version of this step.

### Skeleton — `src/download.py`

```python
import json
import time
from pathlib import Path
import requests

API_URL = "https://ghibli-api.vercel.app/api/films"
RAW_PATH = Path("data/raw/films_raw.json")


def fetch_films(max_retries: int = 3) -> list:
    """Call the API and return the list of films. Retries on failure."""
    for attempt in range(1, max_retries + 1):
        try:
            # TODO: call requests.get(API_URL, timeout=30)
            # TODO: raise an error if the status code isn't 200
            #       (hint: response.raise_for_status())
            # TODO: parse the JSON, and return the list under the "data" key
            pass
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            # TODO: time.sleep(2 * attempt)
    raise RuntimeError("Failed to fetch data after retries")


def save_raw(data: list, path: Path = RAW_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # TODO: write `data` to `path` as JSON, ensure_ascii=False
    #       (keeps original_title in Japanese readable)
```

### Skeleton — `scripts/01_download.py`

```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.download import fetch_films, save_raw

films = fetch_films()
save_raw(films)
print(f"Saved {len(films)} films.")
```

### Hints
- `timeout=30` avoids hanging forever if the request stalls.
- Keep the raw file untouched afterwards — if cleaning goes wrong, you fix
  `clean.py` and re-run it, not re-download.
- `ensure_ascii=False` keeps `original_title` (e.g. `となりのトトロ`)
  human-readable in the saved file.

### ✅ Checkpoint 2
- `python scripts/01_download.py` creates `data/raw/films_raw.json` with
  exactly 22 films.

---

## 3. Step 2 — Clean the data (`src/clean.py`)

Typical problems in this dataset:

| Problem | What to do |
|---|---|
| `release_date`, `running_time`, `rt_score` are strings that look like numbers | `pd.to_numeric(..., errors="coerce")`, then cast to a nullable `Int64` |
| `people`, `species`, `locations`, `vehicles` are lists of URLs, not directly useful | Replace each with a simple **count** (`len(x)`), e.g. `nb_characters` |
| `original_title_romanised` and `original_title` have accents/Japanese characters | Nothing to "fix" — just make sure you save with `ensure_ascii=False` everywhere |
| Possible duplicate rows if you re-run downloads and append instead of overwrite | `df.drop_duplicates(subset="id")` (cheap safety net even if unlikely here) |

### Skeleton — `src/clean.py`

```python
import pandas as pd

KEEP_COLS = ["id", "title", "original_title", "director", "producer",
             "release_date", "running_time", "rt_score",
             "people", "species", "locations", "vehicles"]


def load_raw(path: str) -> pd.DataFrame:
    # TODO: read the JSON file into a DataFrame
    ...


def clean_films(df: pd.DataFrame) -> pd.DataFrame:
    df = df[KEEP_COLS].copy()

    # TODO 1: convert "release_date", "running_time", "rt_score" to numeric
    #         with errors="coerce", then cast to the nullable "Int64" type

    # TODO 2: replace "people" with "nb_characters" = the length of the list
    #         do the same for species -> nb_species, locations -> nb_locations,
    #         vehicles -> nb_vehicles, then drop the original list columns

    # TODO 3: drop duplicates on "id"

    # TODO 4: sort by "release_date"

    return df


def save_clean(df: pd.DataFrame, csv_path: str, parquet_path: str) -> None:
    # TODO: save to both CSV and Parquet
    ...
```

### Skeleton — `scripts/02_clean.py`

```python
from src.clean import load_raw, clean_films, save_clean

df = load_raw("data/raw/films_raw.json")
df_clean = clean_films(df)
save_clean(df_clean, "data/processed/films_clean.csv",
                       "data/processed/films_clean.parquet")
print(df_clean.shape)
print(df_clean.dtypes)
```

### Hints
- `ValueError: Cannot convert non-finite values`? You called `.astype("Int64")`
  before removing bad values with `pd.to_numeric(..., errors="coerce")` —
  always coerce first, cast second.
- `df["people"].apply(len)` gives you the character count per film in one line.

### ✅ Checkpoint 3
- `data/processed/films_clean.csv` and `.parquet` exist, 22 rows.
- `df["id"].is_unique` is `True`.
- `release_date`, `running_time`, `rt_score` are real numeric columns
  (check with `df.dtypes`), not strings.

---

## 4. Step 3 — Split into per-group files (`src/split.py`)

With only 22 films, splitting by year gives you almost one film per file —
not very useful. **Split by `director` instead**, which groups nicely
(Miyazaki has many films, Takahata several, etc.).

### Skeleton — `src/split.py`

```python
from pathlib import Path
import pandas as pd


def split_by_group(df: pd.DataFrame, group_col: str, out_dir: str) -> None:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    # TODO: loop over df.groupby(group_col), and for each group write a CSV
    #       named after the group value — turn spaces into underscores,
    #       e.g. "Hayao Miyazaki" -> "Hayao_Miyazaki.csv"
```

### Skeleton — `scripts/03_split.py`

```python
import pandas as pd
from src.split import split_by_group

df = pd.read_csv("data/processed/films_clean.csv")
split_by_group(df, "director", "data/final/by_director")
```

### ✅ Checkpoint 4
- `data/final/by_director/` contains one CSV per director (e.g.
  `Hayao_Miyazaki.csv` with several rows), and the total row count across
  all files equals 22.

---

## 5. (Bonus) Step 4 — Basic statistics per group

```python
stats = df.groupby("director").agg(
    nb_films=("id", "count"),
    avg_score=("rt_score", "mean"),
    avg_runtime=("running_time", "mean"),
)
```

Try also: the film with the highest `rt_score`, or the average number of
characters (`nb_characters`) per film across the whole studio.

---

## 6. Final verification script

Write a small `scripts/04_check.py` that:

1. Loads `films_clean.csv` and checks it has exactly 22 rows.
2. Asserts `df["id"].is_unique`.
3. Prints `sorted(df["director"].unique())` to eyeball the director list.
4. Loads the `.parquet` version and checks it has the same shape as the CSV.
5. Sums the row counts of every file in `data/final/by_director/*.csv` and
   asserts it equals 22.

---

## 7. Common errors cheat-sheet

| Error | Likely cause | Fix |
|---|---|---|
| `rt_score` stays a string, can't compute `.mean()` | forgot `pd.to_numeric` before using it | `pd.to_numeric(df["rt_score"], errors="coerce")` |
| `ValueError: Cannot convert non-finite values` | `.astype("Int64")` before removing `NaN`s | coerce first, cast second |
| `TypeError: object of type 'float' has no len()` on `people` | a row's `people` list is missing/`NaN` | check with `.isna()` before `.apply(len)`, or `df["people"].apply(lambda x: len(x) if isinstance(x, list) else 0)` |
| File name error when splitting by director | spaces in "Hayao Miyazaki" break some shells/tools | replace spaces with underscores before writing the filename |
| `ModuleNotFoundError: No module named 'src'` | script run from wrong folder | keep the `sys.path.append(...)` line shown above |

---

## 8. Wrap-up on GitHub

```bash
git add .
git commit -m "Pandas pipeline: download, clean, split Studio Ghibli films"
git push
```

Add a short `README.md`: data source, how to run the three scripts in
order, and what each output folder contains (see the separate README
provided for this project).

---

## 9. Going further (optional, once this works)

- Follow one film's `people` URLs (e.g.
  `https://ghibli-api.vercel.app/api/people/<id>`) to fetch character
  details and build a second, richer dataset.
- Add a couple of `pytest` tests for `clean_films` (e.g. a film with a
  missing `rt_score` doesn't crash the pipeline).
- Parameterize `scripts/03_split.py` with `argparse` to choose the group
  column (`director` vs a decade you compute from `release_date`).
- Try `duckdb.sql("SELECT * FROM 'data/processed/*.parquet' WHERE director = 'Hayao Miyazaki'")`.
