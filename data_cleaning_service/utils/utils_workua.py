import numpy as np
import pandas as pd


def parse_salary(salary_str: str) -> (int, int, int):
    """
    Parses salary string into min, max, and average float values.
    Returns (NaN, NaN, NaN) for missing or invalid data.
    """
    if str(salary_str) == '0' or pd.isna(salary_str):
        return np.nan, np.nan, np.nan

    clean_str = str(salary_str).replace(' ', '').replace('\xa0', '')

    if '–' in clean_str:
        parts = clean_str.split('–')
    elif '-' in clean_str:
        parts = clean_str.split('-')
    else:
        try:
            val = float(clean_str)
            return val, val, val
        except ValueError:
            return np.nan, np.nan, np.nan

    try:
        min_val = float(parts[0])
        max_val = float(parts[1])
        avg_val = (min_val + max_val) / 2
        return min_val, max_val, avg_val
    except (ValueError, IndexError):
        return np.nan, np.nan, np.nan
