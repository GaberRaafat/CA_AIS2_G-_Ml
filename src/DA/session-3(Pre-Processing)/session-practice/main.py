from config import DROP_COL_Titanic
from preprocssing import drop_cols
import pandas as pd

df = pd.read_csv('Titanic.csv')

# df = drop_cols(df, DROP_COL_Titanic)

print(df)