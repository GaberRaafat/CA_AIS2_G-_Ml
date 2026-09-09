"""
preprocessing.py

The three functions of session 3 (I copied them, they did not change):
    1- Read_data_file(file_path)
    2- Drop_unnecessary_features(df, cols_to_drop)
    3- Check_data_type(df)

And the new steps that we did in the workshop of session 3, now inside functions:
    4- Check_missing_values(df)
    5- Remove_duplicates(df)
    6- Convert_to_category(df, cols)
    7- Find_outliers(df, num_cols)
    8- Save_data(df, file_path)

The functions are general, they do not know that we are working on insurance.
Everything about the dataset comes from config.py .
"""

import os
import pandas as pd


def Read_data_file(file_path):
    """
    Read a csv file and return a pandas DataFrame.

    If something goes wrong the function prints a short and clear message and
    returns None, so the user does not see a long pandas error.
    """

    # 1) the path must be a text and not empty
    if not isinstance(file_path, str) or file_path.strip() == "":
        print("[ERROR] The path is not valid, please write the path as a text.")
        return None

    # 2) the file must exist
    if not os.path.exists(file_path):
        print(f"[ERROR] The file was not found: {file_path}")
        print("        -> check the name and the folder of the file.")
        return None

    # 3) the path must be a file, not a folder
    if not os.path.isfile(file_path):
        print(f"[ERROR] This path is a folder not a file: {file_path}")
        return None

    # 4) now we try to read it
    try:
        df = pd.read_csv(file_path)

    except pd.errors.EmptyDataError:
        print(f"[ERROR] The file is empty: {file_path}")
        return None

    except pd.errors.ParserError:
        print(f"[ERROR] The file could not be read as a csv: {file_path}")
        print("        -> maybe the separator is not a comma.")
        return None

    except UnicodeDecodeError:
        print(f"[ERROR] The text of the file could not be decoded: {file_path}")
        return None

    except PermissionError:
        print(f"[ERROR] The file is opened by another program or it is protected: {file_path}")
        return None

    except Exception as error:
        # any other problem that I did not think about
        print(f"[ERROR] The file could not be read. ({error})")
        return None

    print(f"[OK] The file was read : {df.shape[0]} rows and {df.shape[1]} columns.")
    return df


def Drop_unnecessary_features(df, cols_to_drop):
    """
    Remove the columns that are inside the list cols_to_drop.

    The list comes from the configuration, so this function works with any
    dataset and not only with one dataset.
    """

    if df is None:
        print("[ERROR] There is no data to work on.")
        return None

    if cols_to_drop is None or len(cols_to_drop) == 0:
        print("[INFO] The list of columns is empty, nothing was removed.")
        return df

    # I drop only the columns that really exist, if not pandas gives a KeyError
    columns_found = [col for col in cols_to_drop if col in df.columns]
    columns_not_found = [col for col in cols_to_drop if col not in df.columns]

    if len(columns_not_found) > 0:
        print(f"[WARNING] These columns are not in the data so I ignored them: {columns_not_found}")

    if len(columns_found) == 0:
        print("[INFO] No column was removed.")
        return df

    new_df = df.drop(columns=columns_found)
    print(f"[OK] {len(columns_found)} column(s) removed: {columns_found}")
    print(f"     the data now has {new_df.shape[1]} columns.")
    return new_df


def Check_data_type(df, category_limit=15):
    """
    A small data quality report (not only df.dtypes).

    For every column it shows:
        - the datatype
        - the number of unique values
        - the number of the missing values and their ratio
        - a small note if the column looks like a category or not

    The result is returned transposed (columns of the data become the columns
    of the report) so it is easy to read.
    """

    if df is None:
        print("[ERROR] There is no data to check.")
        return None

    if df.shape[0] == 0:
        print("[ERROR] The data is empty, there is nothing to describe.")
        return None

    n_rows = df.shape[0]
    report_rows = []

    for col in df.columns:
        n_unique = df[col].nunique()
        n_missing = df[col].isnull().sum()

        # a small guess about the kind of the column
        is_number = pd.api.types.is_numeric_dtype(df[col])

        if n_unique <= category_limit:
            looks_like = "category"
        elif is_number:
            looks_like = "numeric"
        else:
            looks_like = "text"

        report_rows.append({
            "Column": col,
            "Dtype": str(df[col].dtype),
            "N_unique": n_unique,
            "N_missing": n_missing,
            "Missing_%": round((n_missing / n_rows) * 100, 2),
            "Looks_like": looks_like,
        })

    report = pd.DataFrame(report_rows)
    report = report.set_index("Column")

    # transpose -> every column of the data becomes a column in the report
    return report.T


# ----------------------------------------------------------------------------
# the new functions (the steps of the workshop of session 3)
# ----------------------------------------------------------------------------


def Check_missing_values(df):
    """
    A small table with the missing values of every column:
        - the number of the missing values
        - the ratio of the missing values (%)

    It is the same two lines that we wrote in the session (null and ratio)
    but inside a function, so I do not write them again and again.
    """

    if df is None:
        print("[ERROR] There is no data to check.")
        return None

    null = df.isnull().sum()
    ratio = (null / df.shape[0]) * 100

    table = pd.DataFrame({"N_missing": null, "Missing_%": ratio.round(2)})

    total = int(null.sum())
    if total == 0:
        print("[OK] There is no missing values in the data.")
    else:
        print(f"[INFO] There is {total} missing value(s) in the data.")

    # transpose so it looks like the report of Check_data_type
    return table.T


def Remove_duplicates(df):
    """
    Search for the rows that are repeated (the same row written two times)
    and remove them. We keep the first one.
    """

    if df is None:
        print("[ERROR] There is no data to work on.")
        return None

    n_duplicates = df.duplicated().sum()

    if n_duplicates == 0:
        print("[OK] There is no duplicated rows.")
        return df

    # reset_index so the index does not have a hole where the row was removed
    new_df = df.drop_duplicates().reset_index(drop=True)
    print(f"[OK] {n_duplicates} duplicated row(s) removed.")
    print(f"     the data now has {new_df.shape[0]} rows.")
    return new_df


def Convert_to_category(df, cols):
    """
    Change the datatype of the columns in the list to 'category'.

    In the session we converted ALL the columns to category and after that we
    had to convert Age and Fare back to numbers. So here the function takes
    only the columns that we want (the list comes from config.py).
    """

    if df is None:
        print("[ERROR] There is no data to work on.")
        return None

    if cols is None or len(cols) == 0:
        print("[INFO] The list of columns is empty, nothing was converted.")
        return df

    columns_found = [col for col in cols if col in df.columns]
    columns_not_found = [col for col in cols if col not in df.columns]

    if len(columns_not_found) > 0:
        print(f"[WARNING] These columns are not in the data so I ignored them: {columns_not_found}")

    if len(columns_found) == 0:
        print("[INFO] No column was converted.")
        return df

    # I work on a copy so the original DataFrame does not change
    new_df = df.copy()
    new_df[columns_found] = new_df[columns_found].astype("category")

    print(f"[OK] {len(columns_found)} column(s) converted to category: {columns_found}")
    return new_df


def Find_outliers(df, num_cols):
    """
    Find the outliers with the IQR rule that we took in the session:

        IQR         = Q3 - Q1
        lower fence = Q1 - 1.5 * IQR
        upper fence = Q3 + 1.5 * IQR

    every value smaller than the lower fence or bigger than the upper fence
    is an outlier.

    (in the session we wrote  Q1 + 1.5 * IQR  for the upper fence by mistake,
     the correct one is Q3, so I fixed it here)

    The function does NOT remove anything, it only returns a small report
    with one row for every numeric column.
    """

    if df is None:
        print("[ERROR] There is no data to check.")
        return None

    if num_cols is None or len(num_cols) == 0:
        print("[INFO] The list of columns is empty, nothing to check.")
        return None

    n_rows = df.shape[0]
    report_rows = []

    for col in num_cols:
        if col not in df.columns:
            print(f"[WARNING] The column '{col}' is not in the data so I ignored it.")
            continue

        if not pd.api.types.is_numeric_dtype(df[col]):
            print(f"[WARNING] The column '{col}' is not numeric so I ignored it.")
            continue

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_fence = Q1 - 1.5 * IQR
        upper_fence = Q3 + 1.5 * IQR

        n_low = (df[col] < lower_fence).sum()
        n_high = (df[col] > upper_fence).sum()

        report_rows.append({
            "Column": col,
            "Q1": round(Q1, 2),
            "Q3": round(Q3, 2),
            "IQR": round(IQR, 2),
            "Lower_fence": round(lower_fence, 2),
            "Upper_fence": round(upper_fence, 2),
            "N_low_outliers": n_low,
            "N_high_outliers": n_high,
            "Outliers_%": round(((n_low + n_high) / n_rows) * 100, 2),
        })

    if len(report_rows) == 0:
        print("[INFO] No column was checked.")
        return None

    report = pd.DataFrame(report_rows)
    report = report.set_index("Column")

    print(f"[OK] The outliers were checked in {len(report_rows)} column(s).")
    return report


def Save_data(df, file_path):
    """
    Save the clean data in a csv file.
    If the folder does not exist the function creates it.
    """

    if df is None:
        print("[ERROR] There is no data to save.")
        return False

    folder = os.path.dirname(file_path)
    if folder != "" and not os.path.exists(folder):
        os.makedirs(folder)

    try:
        df.to_csv(file_path, index=False)

    except PermissionError:
        print(f"[ERROR] The file is opened by another program (maybe Excel), close it and try again: {file_path}")
        return False

    except Exception as error:
        print(f"[ERROR] The file could not be saved. ({error})")
        return False

    print(f"[OK] The clean data was saved : {file_path}")
    print(f"     {df.shape[0]} rows and {df.shape[1]} columns.")
    return True
