import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.download import fetch_data,save_data

films = fetch_data()
save_data(films)
print(f"Saved {len(films)} films.")