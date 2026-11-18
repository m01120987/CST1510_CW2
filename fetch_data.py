"""
fetch_data.py - Week 8: get data from an API and save it as DATA/raw.csv.

Run it:  python fetch_data.py
"""

from pathlib import Path
import pandas as pd
import requests

# ---- Settings -----------------------------------------------------------

URL = "https://api.github.com/orgs/python/repos"
PARAMS = {"per_page": 100}
RECORDS_KEY = None  # the key that holds the list of records (None if the reply is already a list)

KEEP_COLUMNS = ["name", "language", "stargazers_count", "forks_count", "open_issues_count", "size", "created_at"]
MANDATORY_COLUMN = ["language"]

RAW_FILE_PATH = Path(__file__).parent / "DATA" / "raw.csv"

# ---- The functions ----------------------------------------------------------


def get_data(url, params):
    """Ask the API for data. Returns the JSON reply, or None if something went wrong."""
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()          # turns 404, 500 ... into an error
        return response.json()
    except requests.RequestException as error:
        print("Could not get the data:", error)
        return None


def make_table(data, records_key):
    """Turn the JSON reply into a pandas table."""
    records = data[records_key] if records_key else data
    return pd.json_normalize(records, sep="_")      # nested data becomes column a_b


def tidy_data(df):
    """Keep and clean the columns."""
    df = df[KEEP_COLUMNS]
    df = df.dropna(subset=MANDATORY_COLUMN)
    return df


def save_data(df, path):
    """Save the table as a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Successfully saved {len(df)} rows to {path}")


if __name__ == "__main__":
    data = get_data(URL, PARAMS)
    if data is not None:
        table = make_table(data, RECORDS_KEY)
        cleaned_table = tidy_data(table)
        print("Cleaned table preview:")
        print(cleaned_table.head())
        save_data(cleaned_table, RAW_FILE_PATH)
