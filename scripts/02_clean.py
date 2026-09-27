# -*- coding: utf-8 -*- 
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.clean import cleaning_data

base=Path("data/raw/films_raw.json")

clean_data = cleaning_data(base)
print(clean_data)
# print(f"Saved {len(films.headers)} films.")