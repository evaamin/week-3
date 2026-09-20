from collections import defaultdict

import seaborn as sns
import pandas as pd


# nth Fibonacci number
def fibonacci(n):
    if n < 2:
        return n  # base case: F(0)=0, F(1)=1
    return fibonacci(n - 1) + fibonacci(n - 2)  # F(n) = F(n-1) + F(n-2)


# integer to binary, digit by digit
def to_binary(n):
    if n < 2:
        return str(n)  # base case: 0/1 are their own binary digit
    # bits of n // 2, then the last bit
    return to_binary(n // 2) + str(n % 2)


# Bellevue Almshouse dataset
url = ('https://github.com/melaniewalsh/Intro-Cultural-Analytics/'
       'raw/master/book/data/bellevue_almshouse_modified.csv')
df_bellevue = pd.read_csv(url)


# gender has stray '?', 'g', 'h' codes; treat them as missing
def _clean_gender(df):
    # anything not m/w is bad data
    invalid = ~df['gender'].isin(['m', 'w'])
    if invalid.any():
        codes = sorted(df.loc[invalid, 'gender'].unique())
        print(f"gender: found {invalid.sum()} invalid codes {codes}, "
              f"treating as missing")
    return df['gender'].where(~invalid)  # blank out invalid codes


# columns sorted from least to most missing values
def task_1():
    df = df_bellevue.copy()
    df['gender'] = _clean_gender(df)
    # NaN counts per column, ascending
    return df.isna().sum().sort_values(kind='stable').index.tolist()


# total admissions per year
def task_2():
    # extract year from date
    year = pd.to_datetime(df_bellevue['date_in']).dt.year
    return (
        year.value_counts()  # rows per year
        .sort_index()  # chronological order
        .rename_axis('year')
        .reset_index(name='total_admissions')
    )


# average age by gender
def task_3():
    df = df_bellevue.copy()
    df['gender'] = _clean_gender(df)
    return df.groupby('gender')['age'].mean()


# 5 most common professions, most common first
def task_4():
    return df_bellevue['profession'].value_counts().head(5).index.tolist()


# bonus: memoized nth Fibonacci number
_fib_cache = defaultdict(int)
_fib_cache[0], _fib_cache[1] = 0, 1


def fibonacci_memo(n):
    if n not in _fib_cache:
        # cache miss: compute once, store for every future call
        _fib_cache[n] = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    return _fib_cache[n]
