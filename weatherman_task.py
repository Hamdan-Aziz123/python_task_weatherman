import argparse
import os
import csv
import glob
from datetime import datetime

# random comment just to chnage for new branch and push

RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

MONTH_MAP = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

# This is helper class which is responsible for tasks like
# readings folders,files,parse date


class WeatherDataLoader:
    def find_files_for_year(self, folder, year):
        pattern = os.path.join(folder, f"*{year}_*.txt")
        files = glob.glob(pattern)
        return files

    def find_file_for_month(self, folder, year, month):
        month_abbr = MONTH_MAP.get(month)
        if not month_abbr:
            print(f"Error: Invalid month number {month}")
            return None

        pattern = os.path.join(folder, f"*{year}_{month_abbr}.txt")
        files = glob.glob(pattern)

        if not files:
            print(f"Error: No file found for {year}/{month}"
                  f"in folder: {folder}")
            return None

        return files[0]

    def read_weather_file(self, filepath):
        rows = []

        with open(filepath, 'r') as f:
            content = f.read()

        # Remove empty line at start and HTML comment line at end (<!--)
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

    def safe_int(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d")
        except ValueError:
            return None
# This is the main tasks class , which are performing tasks assigned and
# printing required outputs on screen


class WeatherReporter:

    def __init__(self, folder):

        self.folder = folder
        self.loader = WeatherDataLoader()

    def print_bar(self, day_num, temp, color):

        bar = '+' * temp
        print(f"{day_num:02d} {color}{bar}{RESET} {temp}C")

    def yearly_extremes(self, year):
        # self.loader calls WeatherDataLoader's method
        # self.folder uses the folder stored in __init__
        files = self.loader.find_files_for_year(self.folder, year)

        if not files:
            print(f"No weather files found for year {year} in: {self.folder}")
            return

        max_temp = None
        max_temp_date = None
        min_temp = None
        min_temp_date = None
        max_humid = None
        max_humid_date = None

        for filepath in files:
            rows = self.loader.read_weather_file(filepath)

            for row in rows:
                date = self.loader.parse_date(row.get('PKT', ''))
                if not date:
                    continue

                high = self.loader.safe_int(row.get('Max TemperatureC'))
                low = self.loader.safe_int(row.get('Min TemperatureC'))
                humid = self.loader.safe_int(row.get('Max Humidity'))

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
            print(f"Humid:   {max_humid}% on"
                  f" {max_humid_date.strftime('%B %d')}")
        else:
            print("Humid: No data")

    def monthly_averages(self, year, month):
        filepath = self.loader.find_file_for_month(self.folder, year, month)
        if not filepath:
            return

        rows = self.loader.read_weather_file(filepath)

        high_temps = []
        low_temps = []
        humidities = []

        for row in rows:
            high = self.loader.safe_int(row.get('Max TemperatureC'))
            low = self.loader.safe_int(row.get('Min TemperatureC'))
            humid = self.loader.safe_int(row.get('Mean Humidity'))

            if high is not None:
                high_temps.append(high)
            if low is not None:
                low_temps.append(low)
            if humid is not None:
                humidities.append(humid)

        avg_high = (
            round(sum(high_temps) / len(high_temps))
            if high_temps else "N/A"
        )
        avg_low = (
            round(sum(low_temps) / len(low_temps))
            if low_temps else "N/A"
        )
        avg_humid = (
            round(sum(humidities) / len(humidities))
            if humidities else "N/A"
        )

        month_name = datetime(year, month, 1).strftime("%B %Y")
        print(f"\nMonthly Averages for {month_name}:")
        print("-" * 35)
        print(f"Highest Average: {avg_high}C")
        print(f"Lowest Average:  {avg_low}C")
        print(f"Average Humidity: {avg_humid}%")

    def bar_chart(self, year, month, bonus=False):
        filepath = self.loader.find_file_for_month(self.folder, year, month)
        if not filepath:
            return

        rows = self.loader.read_weather_file(filepath)
        month_name = datetime(year, month, 1).strftime("%B %Y")

        print(f"\n{month_name}")
        print("-" * 50)

        for row in rows:
            date = self.loader.parse_date(row.get('PKT', ''))
            if not date:
                continue

            high = self.loader.safe_int(row.get('Max TemperatureC'))
            low = self.loader.safe_int(row.get('Min TemperatureC'))

            day = date.day

            if not bonus:
                if high is not None:
                    self.print_bar(day, high, RED)
                if low is not None:
                    self.print_bar(day, low, BLUE)
            else:
                if high is not None and low is not None:
                    blue_part = f"{BLUE}{'+' * low}{RESET}"
                    red_part = f"{RED}{'+' * high}{RESET}"
                    print(f"{day:02d} {blue_part}{red_part} {low}C - {high}C")
                elif high is not None:
                    self.print_bar(day, high, RED)
                elif low is not None:
                    self.print_bar(day, low, BLUE)
# This is like starting class handeling parser and then
# calling function from reporter class according to given arguments in parser


class WeatherMan:
    def __init__(self):

        self.reporter = None
        self.parser = argparse.ArgumentParser(
            description="WeatherMan - Lahore Weather Report Generator",
            epilog="""
Examples:
  python3 weatherman_oop.py -e 2004 ~/Downloads/lahore_weather
  python3 weatherman_oop.py -a 2004/6 ~/Downloads/lahore_weather
  python3 weatherman_oop.py -c 2004/6 ~/Downloads/lahore_weather
  python3 weatherman_oop.py -c 2004/6 ~/Downloads/lahore_weather --bonus
            """
        )
        # Call setup as soon as object is created
        self.setup_args()

    def parse_year_month(self, value):
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

    def setup_args(self):
        group = self.parser.add_mutually_exclusive_group(required=True)

        group.add_argument(
            '-e',
            metavar='YEAR',
            type=int,
            help='Show yearly extremes: hottest, coldest, most humid day'
        )

        group.add_argument(
            '-a',
            metavar='YEAR/MONTH',
            type=self.parse_year_month,
            help='Show monthly averages: avg high temp,'
            ' avg low temp, avg humidity'
        )

        group.add_argument(
            '-c',
            metavar='YEAR/MONTH',
            type=self.parse_year_month,
            help='Show bar chart of daily high/low temps for a month'
        )

        self.parser.add_argument(
            '--bonus',
            action='store_true',
            help='(With -c) Show combined single-line bar chart'
            ' instead of two lines'
        )

        self.parser.add_argument(
            'path',
            help='Path to the folder containing weather .txt files'
        )

    def run(self):
        args = self.parser.parse_args()

        if not os.path.isdir(args.path):
            print(f"Error: '{args.path}' is not a valid directory.")
            return

        # Create WeatherReporter object NOW — because now we know the folder
        # self.reporter stores it so we can call methods on it below
        self.reporter = WeatherReporter(args.path)

        if args.e is not None:
            self.reporter.yearly_extremes(args.e)

        elif args.a is not None:
            year, month = args.a
            self.reporter.monthly_averages(year, month)

        elif args.c is not None:
            year, month = args.c
            self.reporter.bar_chart(year, month, bonus=args.bonus)


if __name__ == "__main__":
    app = WeatherMan()
    app.run()


# # *******************************INSTRUCTION********************


# # # flake8 pep 8
# # pre commit ,before commit


# # *******************************commands ********************


# # # Report 1 — Yearly extremes
# # python3 weatherman_task.py -e 2004 ~/Downloads/lahore_weather

# # # Report 2 — Monthly averages
# # python3 weatherman_task.py -a 2004/6 ~/Downloads/lahore_weather

# # # Report 3 — Two-line bar chart
# # python3 weatherman_task.py -c 2004/6 ~/Downloads/lahore_weather

# # # Report 4 (Bonus) — Single combined bar chart
# # python3 weatherman_task.py -c 2004/6 ~/Downloads/lahore_weather --bonus
