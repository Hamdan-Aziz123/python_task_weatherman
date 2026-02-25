# 🌤️ WeatherMan

A command-line weather reporting tool that reads historical weather data files and generates reports for a given year or month.

---


## 🚀 How to Run

### Format
```bash
python3 weatherman_task.py <flag> <value> <path_to_data_folder>
```

---

### Report 1 — Yearly Extremes
Displays the **highest temperature**, **lowest temperature**, and **most humid day** for a given year.

```bash
# Format
python3 weatherman_task.py -e <year> <path>

# Example
python3 weatherman_task.py -e 2004 ~/Downloads/lahore_weather
```

**Output:**
```
Yearly Extremes for 2004:
-----------------------------------
Highest: 45C on June 23
Lowest:  01C on December 22
Humid:   95% on August 14
```

---

### Report 2 — Monthly Averages
Displays the **average highest**, **average lowest** temperature and **average humidity** for a given month.

```bash
# Format
python3 weatherman_task.py -a <year>/<month> <path>

# Example
python3 weatherman_task.py -a 2004/6 ~/Downloads/lahore_weather
```

**Output:**
```
Monthly Averages for June 2004:
-----------------------------------
Highest Average: 39C
Lowest Average:  18C
Average Humidity: 71%
```

---

### Report 3 — Bar Chart (Two Lines Per Day)
Draws a **horizontal bar chart** for each day of a month.
🔴 Red bar = highest temp &nbsp;&nbsp; 🔵 Blue bar = lowest temp

```bash
# Format
python3 weatherman_task.py -c <year>/<month> <path>

# Example
python3 weatherman_task.py -c 2004/6 ~/Downloads/lahore_weather
```

**Output:**
```
June 2004
--------------------------------------------------
01 ++++++++++++++++++++++++++++++++++++++++++ 42C
01 ++++++++++++++++++++++++++++++ 30C
02 +++++++++++++++++++++++++++++++++++++++++ 40C
02 +++++++++++++++++++++++++++ 27C
```

---

### Report 4 — Bar Chart Bonus (Single Line Per Day)
Same as Report 3 but draws **one combined line** per day.
🔵 Blue = lowest temp → 🔴 Red = highest temp

```bash
# Format
python3 weatherman_task.py -c <year>/<month> <path> --bonus

# Example
python3 weatherman_task.py -c 2004/6 ~/Downloads/lahore_weather --bonus
```

**Output:**
```
June 2004
--------------------------------------------------
01 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 30C - 42C
02 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 27C - 40C
```

---

## 🗂️ Data File Format

Each `.txt` file contains weather data for one month. Files follow this naming pattern:

```
lahore_weather_<year>_<month>.txt

Example: lahore_weather_2004_Jun.txt
```

---

## 💡 Flags Summary

| Flag | Input | Description |
|------|-------|-------------|
| `-e` | `YEAR` | Yearly extremes |
| `-a` | `YEAR/MONTH` | Monthly averages |
| `-c` | `YEAR/MONTH` | Bar chart (two lines) |
| `-c --bonus` | `YEAR/MONTH` | Bar chart (one combined line) |

---
