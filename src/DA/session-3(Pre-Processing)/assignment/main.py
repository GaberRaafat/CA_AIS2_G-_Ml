"""
main.py

This file runs the pipeline:
    1- read the titanic file
    2- the user can remove the unnecessary features (the list is saved in config.py)
    3- the user can check the datatypes (small data quality report)

To run it:  python main.py
"""

import pandas as pd

from config import DATA_PATH, COLS_TO_DROP, CATEGORY_LIMIT
from preprocessing import Read_data_file, Drop_unnecessary_features, Check_data_type

# to see all the columns in the terminal
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


def show_menu():
    print("\n=============== Titanic Preprocessing ===============")
    print("1 - Show the first rows of the data")
    print("2 - Remove the unnecessary features")
    print("3 - Check the datatypes (data quality report)")
    print("4 - Exit")


def ask_for_columns():
    """
    Ask the user if he wants to use the list saved in config.py or to write
    his own columns. It returns the list of the columns to remove.
    """
    print(f"The columns saved in config.py are : {COLS_TO_DROP}")
    answer = input("Do you want to use this list ? (y/n) : ").strip().lower()

    if answer == "n":
        typed = input("Write the columns separated by a comma : ")
        # split the text and remove the extra spaces
        return [col.strip() for col in typed.split(",") if col.strip() != ""]

    return COLS_TO_DROP


def main():
    # ---- step 1 : read the data ----
    df = Read_data_file(DATA_PATH)

    if df is None:
        print("The pipeline stopped because the file was not read.")
        return

    # ---- step 2 and 3 : the user chooses ----
    while True:
        show_menu()
        choice = input("Choose a number from 1 to 4 : ").strip()

        if choice == "1":
            print(df.head())

        elif choice == "2":
            cols = ask_for_columns()
            df = Drop_unnecessary_features(df, cols)
            print(df.head())

        elif choice == "3":
            report = Check_data_type(df, CATEGORY_LIMIT)
            print("\n---------- Data Quality Report ----------")
            print(report)

        elif choice == "4":
            print("Good bye :)")
            break

        else:
            print("Wrong choice, please choose a number from 1 to 4.")


if __name__ == "__main__":
    main()
