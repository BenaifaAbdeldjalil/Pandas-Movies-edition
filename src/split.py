# -*- coding: utf-8 -*- 
import pandas as pd
from pathlib import Path
import json 
import numpy as np

def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(
        path,
        encoding="utf-8"
    )

def split_data(df: pd.DataFrame, output_dir: Path):

    output_dir.mkdir(parents=True, exist_ok=True)
    created_files = []

    for cat, group in df.groupby("category"):
        file_path = output_dir / f"slice_{cat}.csv"
        group.to_csv(file_path, index=False, encoding="utf-8")
        created_files.append(file_path)

    print(f"{len(created_files)} departement file created in {output_dir}")
    return created_files

def split(input,output):
    df = load_data(input)
    split_data(df,output)


def check(df):
    df = df
    stats = (
        df.groupby("category")
        .agg(
            nb_products=("id", "count"),
            avg_price=("price", "mean"),
            avg_rating=("rating", "mean"),
            total_stock=("stock", "sum"),
            
        )
        .sort_values("nb_products", ascending=False)
    )

    return(stats)