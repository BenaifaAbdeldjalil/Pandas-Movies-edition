# -*- coding: utf-8 -*- 
import pandas as pd
from pathlib import Path
import json 

def load_data(path : Path) -> pd.DataFrame:
    with open(path,"r",encoding="utf-8") as f:
        data=json.load(f)
    df=pd.json_normalize(data["products"],max_level=None)
    return(df)


def remouve_column(df )-> pd.DataFrame:
    df=df
    column=['sku', 'weight','warrantyInformation', 'shippingInformation', 'availabilityStatus',
       'reviews', 'returnPolicy', 'images','thumbnail', 'meta.barcode','meta.qrCode']
    df=df.drop(column=column)
    return df
def rename_column (df)-> pd.DataFrame:
    column={'discountPercentage':'discount',
            'dimensions.width' :'dimensions_width' , 
            'dimensions.height':'dimensions_height', 
            'dimensions.depth' : 'dimensions_depth',
            'meta.createdAt' : 'dt_creation', 
            'meta.updatedAt' :'dt_update'}
    return (df.rename(columns=column))

def convert_date (df)-> pd.DataFrame:
    column=['dt_creation', 'dt_update']
    for i in column:
        s= pd.to_datetime(df[i],format="ISO8601",utc=True, errors="coerce")
        df[i]=(s.dt.year * 10000 + s.dt.month * 100 + s.dt.day).astype("Int64")
    return (df)


def duplicate_data(df)-> pd.DataFrame:
    df.drop_duplicates(subset=["title","category"])
    return (df)

