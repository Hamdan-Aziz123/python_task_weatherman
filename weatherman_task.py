import argparse
import os
import csv
import glob
from datetime import datetime

RED = "\033[91m"   # Bright red
BLUE = "\033[94m"   # Bright blue
RESET = "\033[0m"    # Resets color


MONTH_MAP = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}


def find_files_for_year(folder, year):
    pattern = os.path.join(folder, f"*{year}_*.txt")
    files = glob.glob(pattern)
    return files


def find_file_for_month(folder, year, month):
    month_abbr = MONTH_MAP.get(month)
    if not month_abbr:
        print(f"Error: Invalid month number {month}")
        return None

    pattern = os.path.join(folder, f"*{year}_{month_abbr}.txt")
    files = glob.glob(pattern)

    if not files:
        print(f"Error: No file found for {year}/{month} in folder: {folder}")
        return None

    return files[0]


def read_weather_file(filepath):
    rows = []

    with open(filepath, 'r') as f:
        content = f.read()

    """
    Remove HTML comment lines like last line in file <!-- 0.261:0 --> and
    first empty line
    """
    lines = [
        line for line in content.splitlines()
        if line.strip() != "" and not line.strip().startswith("<!--")
    ]

    reader = csv.DictReader(lines)

    reader.fieldnames = [field.strip() for field in reader.fieldnames]

    for row in reader:
        clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
        rows.append(clean_row)

    return rows


def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        return None


def report_yearly_extremes(year, folder):
    files = find_files_for_year(folder, year)

    if not files:
        print(f"No weather files found for year {year} in: {folder}")
        return

    max_temp = None
    max_temp_date = None
    min_temp = None
    min_temp_date = None
    max_humid = None
    max_humid_date = None

    for filepath in files:
        rows = read_weather_file(filepath)

        for row in rows:
            date = parse_date(row.get('PKT', ''))
            if not date:
                continue

            high = safe_int(row.get('Max TemperatureC'))
            low = safe_int(row.get('Min TemperatureC'))
            humid = safe_int(row.get('Max Humidity'))

            if high is not None:
                if max_temp is None or high > max_temp:
                    max_temp = high
                    max_temp_date = date

            if low is not None:
                if min_temp is None or low < min_temp:
                    min_temp = low
                    min_temp_date = date

            if humid is not None:
                if max_humid is None or humid > max_humid:
                    max_humid = humid
                    max_humid_date = date

    print(f"\nYearly Extremes for {year}:")
    print("-" * 35)

    if max_temp_date:
        print(f"Highest: {max_temp}C on {max_temp_date.strftime('%B %d')}")
    else:
        print("Highest: No data")

    if min_temp_date:
        print(f"Lowest:  {min_temp}C on {min_temp_date.strftime('%B %d')}")
    else:
        print("Lowest: No data")

    if max_humid_date:
        print(f"Humid:   {max_humid}% on {max_humid_date.strftime('%B %d')}")
    else:
        print("Humid: No data")


def report_monthly_averages(year, month, folder):
    filepath = find_file_for_month(folder, year, month)
    if not filepath:
        return

    rows = read_weather_file(filepath)

    high_temps = []
    low_temps = []
    humidities = []

    for row in rows:
        high = safe_int(row.get('Max TemperatureC'))
        low = safe_int(row.get('Min TemperatureC'))
        humid = safe_int(row.get('Mean Humidity'))

        if high is not None:
            high_temps.append(high)
        if low is not None:
            low_temps.append(low)
        if humid is not None:
            humidities.append(humid)

    avg_high = (
        round(sum(high_temps) / len(high_temps))
        if high_temps
        else "N/A"
    )
    avg_low = (
        round(sum(low_temps) / len(low_temps))
        if low_temps
        else "N/A"
    )

    avg_humid = (
        round(sum(humidities) / len(humidities))
        if humidities
        else "N/A"
    )

    month_name = datetime(year, month, 1).strftime("%B %Y")
    print(f"\nMonthly Averages for {month_name}:")
    print("-" * 35)
    print(f"Highest Average: {avg_high}C")
    print(f"Lowest Average:  {avg_low}C")
    print(f"Average Humidity: {avg_humid}%")


def print_bar(day_num, temp, color):
    bar = '+' * temp   # One '+' per degree
    print(f"{day_num:02d} {color}{bar}{RESET} {temp}C")


def report_bar_chart(year, month, folder, bonus=False):
    filepath = find_file_for_month(folder, year, month)
    if not filepath:
        return

    rows = read_weather_file(filepath)
    month_name = datetime(year, month, 1).strftime("%B %Y")

    print(f"\n{month_name}")
    print("-" * 50)

    for row in rows:
        date = parse_date(row.get('PKT', ''))
        if not date:
            continue

        high = safe_int(row.get('Max TemperatureC'))
        low = safe_int(row.get('Min TemperatureC'))

        day = date.day

        if not bonus:
            if high is not None:
                print_bar(day, high, RED)
            if low is not None:
                print_bar(day, low, BLUE)
        else:
            if high is not None and low is not None:
                blue_part = f"{BLUE}{'+' * low}{RESET}"
                red_part = f"{RED}{'+' * high}{RESET}"
                print(f"{day:02d} {blue_part}{red_part} {low}C - {high}C")
            elif high is not None:
                print_bar(day, high, RED)
            elif low is not None:
                print_bar(day, low, BLUE)


def parse_year_month(value):
    try:
        parts = value.split('/')
        if len(parts) != 2:
            raise ValueError
        year = int(parts[0])
        month = int(parts[1])
        if not (1 <= month <= 12):
            raise ValueError
        return year, month
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid format '{value}'. Expected YEAR/MONTH, e.g. 2004/6"
        )


def main():

    parser = argparse.ArgumentParser(
        description="WeatherMan - Lahore Weather Report Generator",
        epilog="""
Examples:
  python weatherman.py -e 2004 ./weather_data
  python weatherman.py -a 2004/6 ./weather_data
  python weatherman.py -c 2004/6 ./weather_data
  python weatherman.py -c 2004/6 ./weather_data --bonus
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '-e',
        metavar='YEAR',
        type=int,
        help='Show yearly extremes: hottest, coldest, most humid day'
    )

    group.add_argument(
        '-a',
        metavar='YEAR/MONTH',
        type=parse_year_month,
        help='Show monthly averages: avg high temp, avg low temp, avg humidity'
    )

    group.add_argument(
        '-c',
        metavar='YEAR/MONTH',
        type=parse_year_month,
        help='Show bar chart of daily high/low temps for a month'
    )

    parser.add_argument(
        '--bonus',
        action='store_true',
        help=(
            'With -c) Show combined single-line bar chart '
            'instead of two lines'
        )
    )

    parser.add_argument(
        'path',
        help='Path to the folder containing weather.txt files'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a valid directory.")
        return

    if args.e is not None:
        report_yearly_extremes(args.e, args.path)

    elif args.a is not None:
        year, month = args.a
        report_monthly_averages(year, month, args.path)

    elif args.c is not None:
        year, month = args.c
        report_bar_chart(year, month, args.path, bonus=args.bonus)


if __name__ == "__main__":
    main()

# *******************************INSTRUCTION********************


# # flake8 pep 8
# pre commit ,before commit
