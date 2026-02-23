import pandas as pd
from config import DB_PATH

COLUMNS = [
    "id","site","title","price","url","location","posted_at"
]

def load_seen():
    try:
        return pd.read_csv(DB_PATH)
    except:
        return pd.DataFrame(columns=COLUMNS)

def save_seen(df):
    df.to_csv(DB_PATH, index=False)