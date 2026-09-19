
import requests as rq
import json
from pathlib import Path
import pandas as pd




data_json=pd.read_json("data/raw/films_raw.json")

df=pd.json_normalize(data_json["products"],max_level=None)
df["meta.updatedAt"].fillna("2026-01-01")

#df=df.drop_duplicates(subset="id",keep=keep)
#df=df.dropna(inplace=True)

print(df.columns)

liste = ['brand', 'sku', 'weight',
       'warrantyInformation', 'shippingInformation', 
       'reviews', 'returnPolicy',  'images',
       'thumbnail', 'dimensions.width', 'dimensions.height',
       'dimensions.depth', 'meta.updatedAt', 'meta.barcode',
       'meta.qrCode']

df=df.drop(columns=liste)

df["create_month"] = pd.to_datetime(
                        df["meta.createdAt"],
                        utc=True,
                        errors="coerce"
                    ).dt.strftime("%Y-%m")

print(df)