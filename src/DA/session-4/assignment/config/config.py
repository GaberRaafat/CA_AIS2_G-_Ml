"""
config.py

All the settings of the project are written here.
The functions inside preprocessing.py must NOT know anything about the insurance
dataset, so everything about the columns is saved here.

This is the same idea of session 3 : I copied the project of the Titanic and I
only changed this file (the functions stayed the same).
"""

import os

# the folder of the project (the folder that contains main.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# where the raw data is saved
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "insurance.csv")

# where the clean data will be saved after the preprocessing
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "insurance_clean.csv")

# the columns that we do not need in the insurance dataset
# In Titanic we removed PassengerId, Name and Ticket.
# Here there is no id column and no name column, the 7 columns look useful,
# so the list is empty (the function must work also with an empty list).
COLS_TO_DROP = []

# a column with unique values less than this number looks like a category
CATEGORY_LIMIT = 15

# the columns that look like a category (I took them from the data quality report)
# sex      -> male / female
# smoker   -> yes / no
# region   -> 4 regions
# children -> 0 to 5, it is a number but it is a small count so I treat it like a category
CATEGORY_COLS = ["sex", "smoker", "region", "children"]

# the numeric columns, I use them to search for the outliers
NUMERIC_COLS = ["age", "bmi", "charges"]
