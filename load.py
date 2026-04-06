import os
import pandas as pd 

from dotenv import load_dotenv
from sqlalchemy import create_engine, Integer, String, Date

load_dotenv()

def load_data(df: pd.DataFrame, file_path: str, table_name: str):
    # load csv file 
    df.to_csv(file_path, index=False) 

    # load to db 
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    db = os.getenv('DB_NAME')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    dtype_map = {
        'event_id': String,
        'name': String,
        'date': Date,       
        'location': String
    }

    df.to_sql(
        name=table_name, 
        con=engine, 
        if_exists='replace', 
        index=False, 
        dtype=dtype_map
    )

    print(f'{table_name} has been successfully created with {len(df)} rows')