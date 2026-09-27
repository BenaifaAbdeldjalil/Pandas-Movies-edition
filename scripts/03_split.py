# -*- coding: utf-8 -*- 
# -*- coding: utf-8 -*- 
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.split import split

input = Path("data/processed/films_clean.csv")
output = Path("data/final")


split(input,output)

