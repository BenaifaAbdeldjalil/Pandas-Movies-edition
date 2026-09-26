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


