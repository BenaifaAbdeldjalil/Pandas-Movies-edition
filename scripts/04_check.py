import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.split import load_data,check

input = Path("data/processed/films_clean.csv")

df=load_data(input)
df=check(df)

print(df)
