import pandas as pd

def drop_cols(df:pd.DataFrame, cols:list[str]) -> pd.DataFrame:
    return df.drop(columns=cols)

