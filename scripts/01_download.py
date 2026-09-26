import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.download import fetch_data,save_data


url="https://dummyjson.com/products/"
base=Path("data/raw/films_raw.json")

films = fetch_data(url)
save_data(data=films,path=base)
# print(f"Saved {len(films.headers)} films.")