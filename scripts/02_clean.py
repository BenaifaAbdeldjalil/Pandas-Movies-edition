# -*- coding: utf-8 -*- 
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.clean import cleaning_data,save_data

base=Path("data/raw/films_raw.json")
output=Path("data/processed/films_clean.csv")
clean_data = cleaning_data(base)
save_data(data= clean_data, path=output)
# print(clean_data)
# print(f"Saved {len(films.headers)} films.")