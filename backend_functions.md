# 📘 Backend Function Specification

This document defines the current backend functions and classes.  
Goal: Provide a structured overview of purpose, inputs, outputs, and status for each implemented feature.

---

## 🧾 1. File Management

### Function: `delete_data_file(file_path="data.csv")`
**Purpose:**  
Deletes a given data file if it exists.

**Args:**  
- `file_path` (`str`): Path to the file to delete. Default: `"data.csv"`.

**Returns:**  
- `bool`: `True` if successfully deleted, `False` otherwise.

**Behavior:**
- Checks if file exists using `os.path.exists()`.  
- Attempts to delete with `os.remove()`.  
- Prints error messages on failure.

**Status:** 🟢 Implemented

---

## ⏱️ 2. Time Data Management

### Class: `TimeDataManager`
**Purpose:**  
Handles storage and retrieval of start times for daily shifts using CSV files.

**Attributes:**
- `filename`: Default `"startzeiten.csv"`
- `times`: Dictionary or list of `(label, time)` pairs.

**Methods:**
- `read_times()`:  
  Reads all entries from CSV → returns list of `(label, time)`.
- `save_times(new_times)`:  
  Writes new `(label, time)` pairs to CSV.
- *(optional future)* `create_initial_file()`:  
  Creates an empty file if it doesn’t exist.

**Dependencies:**  
- Built-in `csv`, `os`

**Status:** 🟢 Implemented

---

## ⌛ 3. Daily Hours Management

### Class: `DailyHoursManager`
**Purpose:**  
Stores and loads daily working hours for each day in a simple CSV format.

**Attributes:**
- `filename`: Default `"daily_hours.csv"`
- `hours`: Dictionary or list of `(day, hours)` pairs.

**Methods:**
- `read_hours()`:  
  Reads hours from file → returns list of `(day, hours)`.
- `save_hours(new_hours)`:  
  Saves provided `(day, hours)` pairs to file.

**Dependencies:**  
- `csv`, `os`

**Status:** 🟢 Implemented

---

## 🚚 4. Daily Tours Management

### Class: `DailyToursManager`
**Purpose:**  
Manages daily route/tour data for each weekday using separate CSV files.

**Attributes:**
- `base_filename`: Filename pattern, default `"data_{weekday}.csv"`

**Methods:**
- `_get_filename(weekday)`:  
  Returns a file name formatted for the given weekday (e.g., `"data_monday.csv"`).  
- `read_data(weekday)`:  
  Reads `(name, tour_number, assignment)` tuples from file.  
  Returns empty list if file doesn’t exist.  
- `save_data(data, weekday)`:  
  Saves a list of tuples to the weekday-specific file.

**Dependencies:**  
- `csv`, `os`

**Status:** 🟢 Implemented

---

## 📊 5. Excel Data Learning

### Function: `learn_data_from_excel(desired_date)`
**Purpose:**  
Extracts specific scheduling data for a given date from `"Personalplanung 2023.xlsx"`.

**Args:**  
- `desired_date` (`datetime.date`): Target date to extract.

**Returns:**  
- `pandas.DataFrame` with columns:
  - `Name`
  - `Stammtour`
  - `Einsatz`

**Behavior:**
- Reads Excel via `pandas.read_excel()` (`openpyxl` engine).  
- Searches row 4 for the matching date column.  
- Extracts rows 20–132 (`B20:C132`).  
- Filters out empty names.  
- Renames columns accordingly.

**Dependencies:**  
- `pandas`, `openpyxl`, `datetime`

**Status:** 🟢 Implemented

---

## 🗓️ 6. Date and Scheduling Utilities

### Function: `get_next_working_day(current_day)`
**Purpose:**  
Determines the next valid working day (skips Sundays and public holidays).

**Args:**  
- `current_day` (`datetime.date`): Starting date.

**Returns:**  
- `datetime.date`: Next valid working day.

**Dependencies:**  
- `workalendar.europe.Germany`

**Status:** 🟢 Implemented

---

### Function: `get_next_file_day(lastdate, filename="Personalplanung 2023.xlsx")`
**Purpose:**  
Finds the next available date entry in the Excel file after a given date.

**Args:**  
- `lastdate` (`datetime.date`): Reference date.  
- `filename` (`str`): Excel filename (default `"Personalplanung 2023.xlsx"`).

**Returns:**  
- `datetime.date`: The next date column found in the Excel file.

**Status:** 🟢 Implemented

---

### Function: `format_date_with_weekday(date_obj)`
**Purpose:**  
Formats a given date with its German weekday name.

**Args:**  
- `date_obj` (`datetime.date`)

**Returns:**  
- `str`: Example → `"Montag 2025-05-12"`

**Status:** 🟢 Implemented

---

## 👷 7. Data Sorting and Grouping

### Function: `sort_workers(df)`
**Purpose:**  
Categorizes workers by their role or assignment type based on Excel data.

**Args:**  
- `df` (`pandas.DataFrame`): DataFrame with columns `Name`, `Stammtour`, `Einsatz`.

**Returns:**  
- `dict[str, pandas.DataFrame]` containing subsets by category:
  - `"Stammfahrer"`
  - `"Springer"`
  - `"Frühdienst"`
  - `"Spätdienst"`
  - `"Innendienst"`
  - `"Firmen"`
  - `"Einweisung"`
  - `"Abrufer"`

**Behavior:**
- Detects numeric tours, special flags (`'s'`, `'FD'`, `'SD'`, etc.)  
- Sorts numeric tours ascending.  
- Groups into DataFrames by type.

**Status:** 🟢 Implemented

---

## ✅ 8. Implementation Summary

| Function / Class | Category | Status |
|------------------|-----------|---------|
| `delete_data_file` | File Management | 🟢 Implemented |
| `TimeDataManager` | Time Data | 🟢 Implemented |
| `DailyHoursManager` | Work Hours | 🟢 Implemented |
| `DailyToursManager` | Tour Management | 🟢 Implemented |
| `learn_data_from_excel` | Excel Data | 🟢 Implemented |
| `get_next_working_day` | Utilities | 🟢 Implemented |
| `get_next_file_day` | Utilities | 🟢 Implemented |
| `format_date_with_weekday` | Utilities | 🟢 Implemented |
| `sort_workers` | Data Grouping | 🟢 Implemented |

---

## 🧩 Notes

- **Data storage:** CSV and Excel files in the project root.  
- **Core dependencies:** `pandas`, `workalendar`, `csv`, `os`, `datetime`.  
- **Purpose:** Provide a reliable data layer for daily route planning and work-time analysis.  
- **Future extensions:** Could include export (PDF), SMS notifications, or statistical learning modules.

---
