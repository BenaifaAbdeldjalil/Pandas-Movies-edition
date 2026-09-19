# Ghibli Data Pipeline

A small Python/pandas pipeline that fetches all Studio Ghibli films from
the free, no-auth [Ghibli API](https://ghibli-api.vercel.app/), cleans the
data, and exports it into a reusable folder structure (raw → processed →
split by director).

Built as a practice project (TP) to get comfortable with `requests` +
`pandas`: dtype cleaning, nullable integers, flattening nested list fields,
and a simple raw/processed/final data pipeline layout — no API key needed.

---

## Project structure

```
ghibli-data-pipeline/
├── data/
│   ├── raw/                  # untouched API response (gitignored)
│   ├── processed/            # cleaned CSV + Parquet (gitignored)
│   └── final/
│       └── by_director/       # one CSV per director
├── src/
│   ├── download.py            # fetch_films(), save_raw()
│   ├── clean.py                 # clean_films(), save_clean()
│   └── split.py                  # split_by_group()
├── scripts/
│   ├── 01_download.py         # calls src/download.py, writes data/raw/
│   ├── 02_clean.py             # calls src/clean.py, writes data/processed/
│   ├── 03_split.py              # calls src/split.py, writes data/final/by_director/
│   └── 04_check.py              # sanity checks on the final output
├── requirements.txt
└── .gitignore
```

`src/` holds reusable, testable functions. `scripts/` holds the small
numbered programs that run them in order — one script per pipeline step.

---

## Data source

- API: [Studio Ghibli API](https://ghibli-api.vercel.app/) — `GET /api/films`
- **No authentication required** — single request returns all 22 films.
- Fields kept: `id`, `title`, `original_title`, `director`, `producer`,
  `release_date`, `running_time`, `rt_score`, plus character/species/
  location/vehicle counts derived from the nested list fields.

---

## Setup

```bash
git clone https://github.com/<your-username>/ghibli-data-pipeline.git
cd ghibli-data-pipeline

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

No API key, no `.env` file needed.

---

## Usage

Run the scripts in order:

```bash
python scripts/01_download.py   # -> data/raw/films_raw.json
python scripts/02_clean.py      # -> data/processed/films_clean.csv / .parquet
python scripts/03_split.py      # -> data/final/by_director/<director>.csv
python scripts/04_check.py      # sanity checks on the whole pipeline
```

Re-running `02_clean.py` or `03_split.py` alone is safe and won't hit the
network again — only `01_download.py` does.

---

## Output

- `data/processed/films_clean.csv` / `.parquet` — full cleaned dataset,
  22 rows, one per film, deduplicated on `id`, sorted by `release_date`.
- `data/final/by_director/<director>.csv` — same columns, split by
  `director` (e.g. `Hayao_Miyazaki.csv`, `Isao_Takahata.csv`).

---

## Notes

- `data/raw/` and `data/processed/` are gitignored — only code is
  committed, not generated data.
- Since the dataset is tiny (22 rows), this project is meant to practice
  the *shape* of a real pipeline (raw → clean → split → verify), not to
  handle "big data" volumes.
