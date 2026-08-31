"""
preprocessing.py

The three functions of the assignment:
    1- Read_data_file(file_path)
    2- Drop_unnecessary_features(df, cols_to_drop)
    3- Check_data_type(df)

The functions are general, they do not know that we are working on Titanic.
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
    dataset and not only with Titanic.
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
