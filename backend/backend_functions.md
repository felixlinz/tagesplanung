# 📘 Backend Function Specification

This document defines all backend components for the Tour Planning and Learning System.  
It includes **implemented functions** and **planned extensions** for data management, analysis, and communication.

---

## ✅ 1. Implemented Functions

### 🧾 delete_data_file(file_path="data.csv")
**Purpose:**  
Deletes a specified data file if it exists.

**Args:**  
- `file_path` (`str`): File path to delete (default: `"data.csv"`)

**Returns:**  
- `bool`: `True` on success, `False` otherwise

**Dependencies:**  
- `os`

---

### ⏱️ Class: TimeDataManager
**Purpose:**  
Handles the reading and writing of start times (shift start/end) in CSV format.

**Attributes:**
- `filename`: Default `"startzeiten.csv"`
- `times`: list of `(label, time)` pairs

**Methods:**
- `read_times()`: Returns list of stored start times  
- `save_times(new_times)`: Saves new `(label, time)` entries

**Dependencies:**  
- `csv`, `os`

---

### ⌛ Class: DailyHoursManager
**Purpose:**  
Stores and retrieves daily work hours.

**Attributes:**
- `filename`: `"daily_hours.csv"`
- `hours`: list of `(day, hours)` pairs

**Methods:**
- `read_hours()`: Reads daily work hours  
- `save_hours(new_hours)`: Saves new hours to CSV

**Dependencies:**  
- `csv`, `os`

---

### 🚚 Class: DailyToursManager
**Purpose:**  
Manages stored tour layouts per weekday as CSV files.

**Attributes:**
- `base_filename`: Default `"data_{weekday}.csv"`

**Methods:**
- `_get_filename(weekday)`: Returns formatted file name  
- `read_data(weekday)`: Reads tour data for given weekday  
- `save_data(data, weekday)`: Saves list of tuples for that day

**Dependencies:**  
- `csv`, `os`

---

### 📊 learn_data_from_excel(desired_date)
**Purpose:**  
Loads and filters Excel data for a specific date.

**Args:**  
- `desired_date` (`datetime.date`)

**Returns:**  
- `pandas.DataFrame` with columns `['Name', 'Stammtour', 'Einsatz']`

**Details:**  
- Reads `"Personalplanung 2023.xlsx"`  
- Locates the matching date column  
- Extracts and cleans relevant rows  

**Dependencies:**  
- `pandas`, `openpyxl`, `datetime`

---

### 🗓️ get_next_working_day(current_day)
**Purpose:**  
Finds the next valid working day, skipping Sundays and German public holidays.

**Args:**  
- `current_day` (`datetime.date`)

**Returns:**  
- `datetime.date`: Next valid day

**Dependencies:**  
- `workalendar.europe.Germany`

---

### 🗂️ get_next_file_day(lastdate, filename="Personalplanung 2023.xlsx")
**Purpose:**  
Finds the next available date in the Excel file after a given date.

**Args:**  
- `lastdate` (`datetime.date`)
- `filename` (`str`)

**Returns:**  
- `datetime.date`: Next date found

---

### 📅 format_date_with_weekday(date_obj)
**Purpose:**  
Formats date into a human-readable German weekday string.

**Returns:**  
- `"Montag 2025-10-15"` etc.

---

### 👷 sort_workers(df)
**Purpose:**  
Groups employees by role or type of assignment.

**Args:**  
- `df` (`pandas.DataFrame`)

**Returns:**  
- `dict[str, DataFrame]` with categories like `"Stammfahrer"`, `"Springer"`, `"Frühdienst"`, etc.

---

## 🚧 2. Planned Extensions

### 📇 Class: ContactManager
**Purpose:**  
Store, edit, and load contact data (e.g. name, phone, role).

**Planned Methods:**
- `save_contacts(contact_list)`
- `load_contacts()`
- `get_contact(name)`

**Storage:** CSV or JSON  
**Dependencies:** `csv` or `json`

---

### 💬 send_sms(contact, message)
**Purpose:**  
Send SMS to a contact with their work assignment.

**Implementation Idea:**  
- Integrate with API like Twilio or MessageBird  
- Handle authentication tokens securely

---

### 🧾 generate_pdf(report_data, file_path)
**Purpose:**  
Export daily or weekly overviews to PDF.

**Implementation Idea:**  
- Use `reportlab` or `fpdf`  
- Include company header, date, and table formatting

---

### 🧍 Class: RoleManager
**Purpose:**  
Store and provide access to role descriptions.

**Planned Methods:**
- `save_roles(role_data)`
- `load_roles()`

**Storage:** CSV or JSON file with columns `["role", "description"]`

---

### 📁 Class: PathManager
**Purpose:**  
Store and retrieve file paths (e.g., to Excel data source).

**Planned Methods:**
- `save_path(path)`
- `load_path()`

---

### 🧠 Function: get_tour_frequency()
**Purpose:**  
Analyze all stored CSVs to determine which delivery person drives which tour most frequently.

**Output:**  
Dictionary `{zusteller_name: {tour_id: frequency}}`

---

### 🏆 Function: get_ranked_tours_by_zusteller(zusteller_name)
**Purpose:**  
Return a ranked list of tours by frequency for a given person.

**Output:**  
List of `(tour_id, frequency)` sorted descending.

---

## 📋 3. Overview Table

| Feature | Function/Class | Status |
|----------|----------------|---------|
| Load Excel data | `learn_data_from_excel()` | 🟢 Implemented |
| Provide DataFrame | `learn_data_from_excel()` | 🟢 Implemented |
| Save/load weekday tour layout | `DailyToursManager` | 🟢 Implemented |
| Save/load daily work hours | `DailyHoursManager` | 🟢 Implemented |
| Save contacts | `ContactManager` | ⚪ Planned |
| Send SMS with assignments | `send_sms()` | ⚪ Planned |
| Export to PDF | `generate_pdf()` | ⚪ Planned |
| Save/load roles | `RoleManager` | ⚪ Planned |
| Save data path | `PathManager` | ⚪ Planned |
| Learn frequent tours | `get_tour_frequency()` | ⚪ Planned |
| Ranked tour list per driver | `get_ranked_tours_by_zusteller()` | ⚪ Planned |

---

## 🧩 Notes

- **Core Libraries:** `pandas`, `csv`, `os`, `datetime`, `workalendar`  
- **File Storage:** CSV and Excel  
- **Planned Libraries:** `reportlab` / `fpdf`, `twilio`, `json`
- **Architecture Goal:** Modular backend for data analysis, daily planning, and communication automation.

---
