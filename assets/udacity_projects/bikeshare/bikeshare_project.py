import os
import time
import pandas as pd

# Constants
DATA_DIR = ""
CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}
VALID_CITIES = list(CITY_DATA.keys())
VALID_MONTHS_INPUT = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
VALID_DAYS_INPUT = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
FULL_MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
MONTH_TO_NUM = {name: i + 1 for i, name in enumerate(VALID_MONTHS_INPUT[1:])} # Moved here for global access

# Helper Functions
def get_user_choice(prompt, valid_options):
    while True:
        choice = input(prompt).lower()
        if choice in valid_options: return choice
        print(f"Invalid input. Please choose from {', '.join(valid_options)}.")

def print_stat_if_available(df, column_name, stat_description, calculation_func):
    (calculation_func(df[column_name]) if column_name in df.columns else \
     print(f"{stat_description} data not available."))

# Main Functions
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = get_user_choice("Would you like to see data for Chicago, New York City, or Washington?\n", VALID_CITIES)
    month = get_user_choice("Which month? All, January, February, March, April, May, or June?\n", VALID_MONTHS_INPUT)
    day = get_user_choice("Which day of the week? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n", VALID_DAYS_INPUT)
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(os.path.join(DATA_DIR, CITY_DATA[city]))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'], df['day_of_week'], df['hour'] = df['Start Time'].dt.month, df['Start Time'].dt.day_name(), df['Start Time'].dt.hour
    df = df[df['month'] == MONTH_TO_NUM[month]] if month != 'all' else df
    df = df[df['day_of_week'] == day.title()] if day != 'all' else df
    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print_stat_if_available(df, 'month', 'Month', lambda s: print(f"Most Common Month: {FULL_MONTH_NAMES[s.mode()[0] - 1]}"))
    print_stat_if_available(df, 'day_of_week', 'Day of week', lambda s: print(f"Most Common Day of Week: {s.mode()[0]}"))
    print_stat_if_available(df, 'hour', 'Start hour', lambda s: print(f"Most Common Start Hour: {s.mode()[0]}:00"))
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print_stat_if_available(df, 'Start Station', 'Start Station', lambda s: print(f"Most Commonly Used Start Station: {s.mode()[0]}"))
    print_stat_if_available(df, 'End Station', 'End Station', lambda s: print(f"Most Commonly Used End Station: {s.mode()[0]}"))
    # One-liner for trip combination check
    (print(f"Most Frequent Trip Combination: {(df['Start Station'] + ' to ' + df['End Station']).mode()[0]}") \
     if 'Start Station' in df.columns and 'End Station' in df.columns \
     else print("Station data not available for trip combinations."))
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print_stat_if_available(df, 'Trip Duration', 'Trip Duration', lambda s: print(f"Total Travel Time: {s.sum():.2f} seconds"))
    print_stat_if_available(df, 'Trip Duration', 'Trip Duration', lambda s: print(f"Mean Travel Time: {s.mean():.2f} seconds"))
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print_stat_if_available(df, 'User Type', 'User Type', lambda s: print("Counts of User Types:\n", s.value_counts()))
    print_stat_if_available(df, 'Gender', 'Gender', lambda s: print("\nCounts of Gender:\n", s.value_counts()))
    # Condensed birth year stats
    if 'Birth Year' in df.columns:
        birth_years = df['Birth Year'].dropna()
        (print(f"\nEarliest Year of Birth: {int(birth_years.min())}\n"
               f"Most Recent Year of Birth: {int(birth_years.max())}\n"
               f"Most Common Year of Birth: {int(birth_years.mode()[0])}") \
         if not birth_years.empty else print("\nBirth Year data available but all values are missing."))
    else: print("\nBirth Year data not available for this city.")
    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        try:
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        except FileNotFoundError: print(f"Error: The data file for {city.title()} was not found. Please ensure it's in the '{os.path.basename(DATA_DIR)}' directory.")
        except KeyError as e: print(f"Error: A required column was not found in the data or an invalid key was used: {e}. This might happen if a column like 'Gender' or 'Birth Year' is missing for a specific city's data.")
        except Exception as e: print(f"An unexpected error occurred: {e}")
        if input('\nWould you like to restart? Enter yes or no.\n').lower() != 'yes': break

if __name__ == "__main__":
    main()