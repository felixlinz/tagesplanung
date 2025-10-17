import csv
import os
from ast import literal_eval

class WeekdayTourListManager:
    """
    Handles storing and retrieving tour lists for each weekday.
    Each weekday corresponds to exactly one CSV file.
    """

    def __init__(self, base_directory: str = "data/weekday_tours"):
        """
        Args:
            base_directory (str): Folder where weekday CSVs are stored.
        """
        self.base_directory = base_directory
        os.makedirs(self.base_directory, exist_ok=True)

    def _get_filename(self, weekday: str) -> str:
        """
        Builds a normalized file path for the given weekday.
        """
        clean_name = weekday.strip().lower()
        filename = f"{clean_name}.csv"
        return os.path.join(self.base_directory, filename)

    def save_tours_for_day(self, weekday: str, tours: list[int]) -> None:
        """
        Saves (or overwrites) the list of tour numbers for a given weekday.

        Args:
            weekday (str): Weekday name (e.g. 'Monday', 'Tuesday').
            tours (list[int]): List of tour IDs to save.
        """
        filename = self._get_filename(weekday)
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Tour"])
            for tour in tours:
                writer.writerow([tour])
        print(f"✅ Saved {len(tours)} tours for {weekday} → {filename}")

    def load_tours_for_day(self, weekday: str) -> list[int]:
        """
        Loads the list of tour numbers for a given weekday.
        Returns an empty list if no file exists.

        Args:
            weekday (str): Weekday name (e.g. 'Monday', 'Tuesday').

        Returns:
            list[int]: Saved tour numbers.
        """
        filename = self._get_filename(weekday)
        if not os.path.exists(filename):
            return []
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            return [int(row["Tour"]) for row in reader]

    def list_saved_weekdays(self) -> list[str]:
        """
        Lists all weekdays for which tour files currently exist.

        Returns:
            list[str]: List of weekday names (e.g. ['monday', 'tuesday'])
        """
        files = os.listdir(self.base_directory)
        return [f.replace(".csv", "") for f in files if f.endswith(".csv")]

    def delete_tours_for_day(self, weekday: str) -> bool:
        """
        Deletes the CSV file for the given weekday, if it exists.

        Returns:
            bool: True if deleted, False otherwise.
        """
        filename = self._get_filename(weekday)
        if os.path.exists(filename):
            os.remove(filename)
            return True
        return False


import os
import csv
from ast import literal_eval

class JobDefinitionManager:
    """
    Manages saving and loading job definitions.
    Each job defines:
      - two time reference names (as strings)
      - a short symbol
      - an RGB color
      - an active flag (boolean)
    """

    def __init__(self, filename: str = "data/job_definitions.csv"):
        """
        Args:
            filename (str): Path to CSV file storing job definitions.
        """
        self.filename = filename
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    def save_jobs(self, job_data: dict[str, dict]) -> None:
        """
        Saves or overwrites all job definitions.

        Args:
            job_data (dict): e.g.
                {
                    "Innendienst": {
                        "time_ref_1": "Frühschicht",
                        "time_ref_2": "Spätschicht",
                        "symbol": "ID",
                        "color": (255, 200, 0),
                        "active": True
                    },
                    ...
                }
        """
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Job",
                "TimeRef1",
                "TimeRef2",
                "Symbol",
                "Color",
                "Active"
            ])
            for job, attrs in job_data.items():
                writer.writerow([
                    job,
                    attrs.get("time_ref_1", ""),
                    attrs.get("time_ref_2", ""),
                    attrs.get("symbol", ""),
                    str(attrs.get("color", "")),
                    int(bool(attrs.get("active", False))),
                ])
        print(f"✅ Saved {len(job_data)} job definitions → {self.filename}")

    def load_jobs(self) -> dict[str, dict]:
        """
        Loads all job definitions.

        Returns:
            dict[str, dict]: e.g.
                {
                    "Innendienst": {
                        "time_ref_1": "Frühschicht",
                        "time_ref_2": "Spätschicht",
                        "symbol": "ID",
                        "color": (255, 200, 0),
                        "active": True
                    },
                    ...
                }
        """
        if not os.path.exists(self.filename):
            return {}

        result = {}
        with open(self.filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                color_value = row.get("Color", "").strip()
                try:
                    color = literal_eval(color_value) if color_value else None
                except (ValueError, SyntaxError):
                    color = color_value  # fallback to raw string if malformed

                result[row["Job"]] = {
                    "time_ref_1": row.get("TimeRef1", ""),
                    "time_ref_2": row.get("TimeRef2", ""),
                    "symbol": row.get("Symbol", ""),
                    "color": color,
                    "active": bool(int(row.get("Active", "0") or 0)),
                }
        return result

    def list_jobs(self) -> list[str]:
        """
        Lists all job names currently stored.

        Returns:
            list[str]
        """
        return list(self.load_jobs().keys())

    def delete_jobs(self) -> bool:
        """
        Deletes the job definitions file.

        Returns:
            bool: True if deleted, False otherwise.
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"🗑️ Deleted {self.filename}")
            return True
        return False


class TimeReferenceManager:
    """
    Manages storing and retrieving time reference values.
    Each time reference is a named variable (string) with an assigned time string.
    Example:
        {
            "Frühschicht": "05:30",
            "Spätschicht": "13:15",
            "Nachtschicht": ""
        }
    """

    def __init__(self, filename: str = "data/time_references.csv"):
        """
        Args:
            filename (str): Path to CSV file where time references are stored.
        """
        self.filename = filename
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    def save_times(self, time_data: dict[str, str]) -> None:
        """
        Saves or overwrites all time references.

        Args:
            time_data (dict): {"Frühschicht": "05:30", "Spätschicht": "13:15", ...}
        """
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Reference", "Time"])
            for ref, time_val in time_data.items():
                # even empty string time values must be written
                writer.writerow([ref, time_val])
        print(f"✅ Saved {len(time_data)} time references → {self.filename}")

    def load_times(self) -> dict[str, str]:
        """
        Loads time references from file.

        Returns:
            dict[str, str]: {"Frühschicht": "05:30", "Spätschicht": "13:15", ...}
        """
        if not os.path.exists(self.filename):
            return {}

        result = {}
        with open(self.filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                ref_name = row.get("Reference", "").strip()
                time_val = row.get("Time", "")
                result[ref_name] = time_val
        return result

    def list_references(self) -> list[str]:
        """
        Returns a list of all stored time reference names.
        """
        return list(self.load_times().keys())

    def delete_times(self) -> bool:
        """
        Deletes the time references file, if it exists.

        Returns:
            bool: True if deleted, False otherwise.
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"🗑️ Deleted {self.filename}")
            return True
        return False


class WeekdayWorktimeManager:
    """
    Manages storing and retrieving required work durations per weekday.
    Each entry maps a weekday name (e.g. 'Montag') to a time string (e.g. '07:45').
    """

    def __init__(self, filename: str = "data/work_durations.csv"):
        """
        Args:
            filename (str): Path to CSV file where weekday work durations are stored.
        """
        self.filename = filename
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    def save_worktimes(self, worktime_data: dict[str, str]) -> None:
        """
        Saves or overwrites weekday work durations.

        Args:
            worktime_data (dict): e.g.
                {"Montag": "07:45", "Dienstag": "08:15", ...}
        """
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Weekday", "Worktime"])
            for weekday, duration in worktime_data.items():
                writer.writerow([weekday, duration])
        print(f"✅ Saved {len(worktime_data)} weekday work durations → {self.filename}")

    def load_worktimes(self) -> dict[str, str]:
        """
        Loads weekday work durations from file.

        Returns:
            dict[str, str]: e.g. {"Montag": "07:45", "Dienstag": "08:15", ...}
        """
        if not os.path.exists(self.filename):
            return {}

        result = {}
        with open(self.filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                weekday = row.get("Weekday", "").strip()
                duration = row.get("Worktime", "")
                result[weekday] = duration
        return result

    def list_weekdays(self) -> list[str]:
        """
        Lists all weekday names currently stored.
        """
        return list(self.load_worktimes().keys())

    def delete_worktimes(self) -> bool:
        """
        Deletes the weekday work durations file.

        Returns:
            bool: True if deleted, False otherwise.
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"🗑️ Deleted {self.filename}")
            return True
        return False
    
class BreakTimeManager:
    """
    Manages storing and retrieving the global break duration.
    Stored as a single time value (e.g. '00:30').
    """

    def __init__(self, filename: str = "data/break_time.csv"):
        """
        Args:
            filename (str): Path to CSV file where the break time is stored.
        """
        self.filename = filename
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    def save_break_time(self, break_data: dict[str, str]) -> None:
        """
        Saves or overwrites the break time.

        Args:
            break_data (dict): e.g. {"Break": "00:30"}
        """
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Time"])
            for name, value in break_data.items():
                writer.writerow([name, value])
        print(f"✅ Saved break time → {self.filename}")

    def load_break_time(self) -> dict[str, str]:
        """
        Loads the break time.

        Returns:
            dict[str, str]: e.g. {"Break": "00:30"}
        """
        if not os.path.exists(self.filename):
            return {}

        with open(self.filename, mode="r") as file:
            reader = csv.DictReader(file)
            return {row["Name"]: row["Time"] for row in reader}

    def get_break_value(self) -> str:
        """
        Returns only the break time value (e.g. '00:30'),
        or an empty string if none exists.
        """
        data = self.load_break_time()
        return next(iter(data.values()), "")

    def delete_break_time(self) -> bool:
        """
        Deletes the break time file.

        Returns:
            bool: True if deleted, False otherwise.
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"🗑️ Deleted {self.filename}")
            return True
        return False
    
class ContactManager:
    """
    Manages storing and retrieving names and phone numbers.
    Data is stored in a single CSV file, with each row as a name–number pair.
    """

    def __init__(self, filename: str = "data/contacts.csv"):
        """
        Args:
            filename (str): Path to CSV file where contacts are stored.
        """
        self.filename = filename
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    def save_contacts(self, contact_data: dict[str, str]) -> None:
        """
        Saves or overwrites all contact data.

        Args:
            contact_data (dict): {"Name": "PhoneNumber", ...}
        """
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone"])
            for name, number in contact_data.items():
                writer.writerow([name, number])
        print(f"✅ Saved {len(contact_data)} contacts → {self.filename}")

    def load_contacts(self) -> dict[str, str]:
        """
        Loads all contacts from the file.

        Returns:
            dict[str, str]: {"Name": "PhoneNumber", ...}
        """
        if not os.path.exists(self.filename):
            return {}

        result = {}
        with open(self.filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get("Name", "").strip()
                phone = row.get("Phone", "").strip()
                result[name] = phone
        return result

    def get_contact(self, name: str) -> str | None:
        """
        Retrieves a single phone number by name.

        Args:
            name (str): The contact name to look up.

        Returns:
            str | None: The phone number, or None if not found.
        """
        contacts = self.load_contacts()
        return contacts.get(name)

    def list_contacts(self) -> list[str]:
        """
        Returns a list of all stored contact names.
        """
        return list(self.load_contacts().keys())

    def delete_contacts(self) -> bool:
        """
        Deletes the contacts file.

        Returns:
            bool: True if deleted, False otherwise.
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"🗑️ Deleted {self.filename}")
            return True
        return False
    
class PathManager:
    """
    Manages storing and retrieving a single filesystem path.
    """

    def __init__(self, filename: str = "path_config.csv"):
        """
        Args:
            filename (str): Path to CSV file where the path is stored.
        """
        self.filename = filename
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    def save_path(self, path_data: dict[str, str]) -> None:
        """
        Saves or overwrites the path configuration.

        Args:
            path_data (dict): e.g. {"BasePath": "C:/Users/Admin/Documents"}
        """
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Path"])
            for name, path in path_data.items():
                writer.writerow([name, path])
        print(f"✅ Saved {len(path_data)} path entries → {self.filename}")

    def load_paths(self) -> dict[str, str]:
        """
        Loads stored paths.

        Returns:
            dict[str, str]: e.g. {"BasePath": "C:/Users/Admin/Documents"}
        """
        if not os.path.exists(self.filename):
            return {}

        result = {}
        with open(self.filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get("Name", "").strip()
                path = row.get("Path", "").strip()
                result[name] = path
        return result

    def get_path(self, name: str) -> str | None:
        """
        Retrieves a stored path by name.

        Args:
            name (str): The key name under which the path was stored.

        Returns:
            str | None: The stored path, or None if not found.
        """
        paths = self.load_paths()
        return paths.get(name)

    def delete_paths(self) -> bool:
        """
        Deletes the path configuration file.

        Returns:
            bool: True if deleted, False otherwise.
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"🗑️ Deleted {self.filename}")
            return True
        return False
    

class EmployeeTaskLogManager:
    """
    Tracks how often each employee performs each task/tour,
    and can report the most experienced employees per task.
    """

    def __init__(self, filename: str = "data/employee_task_log.csv"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    @staticmethod
    def _sort_key(value: str):
        try:
            return (0, int(value))
        except ValueError:
            return (1, value.lower())

    def _load_log(self) -> list[dict]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def _save_log(self, data: list[dict]):
        if not data:
            return
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        task_columns = sorted(
            [k for k in all_keys if k.lower() != "name"],
            key=self._sort_key
        )
        fieldnames = ["Name"] + task_columns
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    def increment_task_count(self, entry: dict[str, str]) -> None:
        if not entry or len(entry) != 1:
            raise ValueError("Entry must contain exactly one {name: task_id} pair.")
        name_input, task_input = next(iter(entry.items()))
        name_norm = name_input.strip().lower()
        task_norm = task_input.strip().lower()

        data = self._load_log()
        name_map = {row["Name"].strip().lower(): row["Name"] for row in data}

        if name_norm not in name_map:
            known_cols = [k for k in data[0].keys() if k.lower() != "name"] if data else []
            new_row = {"Name": name_input}
            for col in known_cols:
                new_row[col] = "0"
            data.append(new_row)
            name_map[name_norm] = name_input

        existing_tasks = {k.lower() for k in data[0].keys() if k.lower() != "name"} if data else set()
        if task_norm not in existing_tasks:
            for row in data:
                row[task_input] = "0"

        for row in data:
            if row["Name"].strip().lower() == name_norm:
                for key in row.keys():
                    if key.lower() == task_norm:
                        current_val = int(row.get(key, "0") or 0)
                        row[key] = str(current_val + 1)
                        print(f"✅ Incremented {row['Name']} – Task {key} → now {row[key]}")
                        break
                break

        self._save_log(data)

    def get_employee_summary(self, name: str) -> dict[str, int]:
        name_norm = name.strip().lower()
        data = self._load_log()
        for row in data:
            if row["Name"].strip().lower() == name_norm:
                return {
                    k: int(v) if k.lower() != "name" else v
                    for k, v in row.items()
                }
        return {}

    def get_all(self) -> list[dict[str, str]]:
        return self._load_log()

    def reset_log(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name"])
        print(f"🧹 Log reset → {self.filename} is now empty.")

    def get_top_employees_for_task(self, task_id: str, top_n: int = 3) -> list[tuple[str, int]]:
        """
        Returns the top N employees with the most experience for a given task.

        Args:
            task_id (str): Task/Tour ID (case-insensitive)
            top_n (int): Number of top employees to return

        Returns:
            list[tuple[str, int]]: e.g. [("Zimmermann", 12), ("Becker", 9), ("Lange", 6)]
        """
        data = self._load_log()
        if not data:
            return []

        task_norm = task_id.strip().lower()
        scores = []

        for row in data:
            # Find column matching task_id (case-insensitive)
            value = 0
            for key, val in row.items():
                if key.lower() == task_norm:
                    try:
                        value = int(val)
                    except (ValueError, TypeError):
                        value = 0
                    break
            scores.append((row["Name"], value))

        # Sort by count desc, then name asc
        scores.sort(key=lambda x: (-x[1], x[0].lower()))

        # Filter out employees with 0 experience
        scores = [(n, v) for n, v in scores if v > 0]

        return scores[:top_n]