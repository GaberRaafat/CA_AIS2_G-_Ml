"""
config.py

All the settings of the project are written here.
The functions inside preprocessing.py must NOT know anything about the Titanic
dataset, so the columns that we want to remove are saved here.
If tomorrow I work on another dataset I only change this file.
"""

import os

# the folder of the project (the folder that contains main.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# where the raw data is saved
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "titanic.csv")

# the columns that we do not need in the Titanic dataset
# PassengerId -> just a counter
# Name        -> a text that is different for every row
# Ticket      -> a code that we can not use like this
COLS_TO_DROP = ["PassengerId", "Name", "Ticket"]

# a column with unique values less than this number looks like a category
CATEGORY_LIMIT = 15
