"""
main.py

This file runs the pipeline:
    1- read the insurance file
    2- the user can remove the unnecessary features (the list is saved in config.py)
    3- the user can check the datatypes (small data quality report)
    4- the user can check the missing values
    5- the user can remove the duplicated rows
    6- the user can convert the categorical columns to category
    7- the user can search for the outliers with the IQR rule
    8- the user can save the clean data

To run it:  python main.py
"""

import pandas as pd

from config import (
    DATA_PATH,
    PROCESSED_PATH,
    COLS_TO_DROP,
    CATEGORY_LIMIT,
    CATEGORY_COLS,
    NUMERIC_COLS,
)
from preprocessing import (
    Read_data_file,
    Drop_unnecessary_features,
    Check_data_type,
    Check_missing_values,
    Remove_duplicates,
    Convert_to_category,
    Find_outliers,
    Save_data,
)

# to see all the columns in the terminal
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


def show_menu():
    print("\n=============== Insurance Preprocessing ===============")
    print("1 - Show the first rows of the data")
    print("2 - Remove the unnecessary features")
    print("3 - Check the datatypes (data quality report)")
    print("4 - Check the missing values")
    print("5 - Remove the duplicated rows")
    print("6 - Convert the categorical columns to category")
    print("7 - Find the outliers (IQR rule)")
    print("8 - Save the clean data")
    print("9 - Exit")


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

    # ---- the other steps : the user chooses ----
    while True:
        show_menu()
        choice = input("Choose a number from 1 to 9 : ").strip()

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
            table = Check_missing_values(df)
            print("\n---------- Missing Values ----------")
            print(table)

        elif choice == "5":
            df = Remove_duplicates(df)

        elif choice == "6":
            df = Convert_to_category(df, CATEGORY_COLS)
            print(pd.DataFrame(df.dtypes, columns=["Dtype"]).T)

        elif choice == "7":
            report = Find_outliers(df, NUMERIC_COLS)
            print("\n---------- Outliers Report (IQR) ----------")
            print(report)

        elif choice == "8":
            Save_data(df, PROCESSED_PATH)

        elif choice == "9":
            print("Good bye :)")
            break

        else:
            print("Wrong choice, please choose a number from 1 to 9.")


if __name__ == "__main__":
    main()
