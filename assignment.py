import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('data.csv')

# Converting the 'Time' and 'Time Out' columns to datetime objects
df['Time'] = pd.to_datetime(df['Time'])
df['Time Out'] = pd.to_datetime(df['Time Out'])

# Calculating duration
df['Time Duration'] = df['Time Out'] - df['Time']

#function to check consecutive days
def check_consecutive_days(series, n=7):
    return any((series - series.shift(1) == timedelta(days=1)).rolling(window=n).sum() == n - 1)

#employees who worked for 7 consecutive days
consecutive_days_condition = df.groupby('Employee Name')['Time'].transform(check_consecutive_days)
employees_7_consecutive_days = df.loc[consecutive_days_condition, 'Employee Name'].unique()

#  employees with less than 10 hours between shifts but greater than 1 hour
df['Time Between Shifts'] = df['Time'].diff()
time_between_shifts_condition = (df['Time Between Shifts'] > timedelta(hours=1)) & (df['Time Between Shifts'] < timedelta(hours=10))
employees_less_than_10_hours = df.loc[time_between_shifts_condition, 'Employee Name'].unique()

# employees who worked for more than 14 hours in a single shift
long_shift_condition = df['Time Duration'] > timedelta(hours=14)
employees_long_shift = df.loc[long_shift_condition, 'Employee Name'].unique()

# results
with open('output.txt', 'w') as file:
    print("Employees who worked for 7 consecutive days:", file=file)
    print(employees_7_consecutive_days, file=file)
    print("\nEmployees with less than 10 hours between shifts but greater than 1 hour:", file=file)
    print(employees_less_than_10_hours, file=file)
    print("\nEmployees who worked for more than 14 hours in a single shift:", file=file)
    print(employees_long_shift, file=file)

