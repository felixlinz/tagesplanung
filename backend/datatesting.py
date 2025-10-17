from excel_file_manager import ExcelManager 
from logicmanager import TourAssigner 
import data_manager
from datetime import date
import pprint

def main():
    daily_hours_test()
    
    
def datalearner_test():
    manager = ExcelManager(date(2025,8,26))
    pprint.pp(manager.sorted)
    
def tourlistenspeicher_test():
    manager = data_manager.WeekdayTourListManager()

    # Save some data
    print(manager.load_tours_for_day("Tuesday"))
  
def job_attribute_test():    
    manager = data_manager.TimeReferenceManager()

    # Save some times
    manager.save_times({
        "Frühschicht": "05:30",
        "Spätschicht": "13:15",
        "Nachtschicht": "",
    })

    # Load them
    times = manager.load_times()
    print(times)
    # → {'Frühschicht': '05:30', 'Spätschicht': '13:15', 'Nachtschicht': ''}

    # List names
    print(manager.list_references())
    # → ['Frühschicht', 'Spätschicht', 'Nachtschicht']


def tour_assigment_test():
    requested_tours = [1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 15, 22, 23, 28, 31, 32, 40, 41, 42, 43, 44, 46]

    manager = ExcelManager(date(2025,8,26))
    pprint.pp(manager.sorted)
    print("______________________")

    assigner = TourAssigner(manager.sorted)
    result = assigner.assign_tours(requested_tours)

    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    
def daily_hours_test():
    manager = data_manager.WeekdayWorktimeManager()

    manager.save_worktimes({
        "Montag": "07:45",
        "Dienstag": "08:15",
        "Mittwoch": "07:30",
        "Donnerstag": "08:00",
        "Freitag": "06:45",
        "Samstag": "07:00",
        "Sonntag": "07:00"
    })

    print(manager.load_worktimes())
    # → {'Montag': '07:45', 'Dienstag': '08:15', 'Mittwoch': '07:30', ...}

    print(manager.list_weekdays())
    # → ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

def break_test():
    manager = data_manager.BreakTimeManager()


    # Or just get the value
    print(manager.get_break_value())
    # → '00:30'

def contact_test():
    manager = data_manager.ContactManager()

    # Save some contacts
    manager.save_contacts({
        "Anna": "+49 172 1234567",
        "Ben": "0157 99887766",
        "Clara": "0170 11223344"
    })

    # Load all contacts
    print(manager.load_contacts())
    # → {'Anna': '+49 172 1234567', 'Ben': '0157 99887766', 'Clara': '0170 11223344'}

    # Get a single contact
    print(manager.get_contact("Ben"))
    # → '0157 99887766'

    # List names
    print(manager.list_contacts())
    # → ['Anna', 'Ben', 'Clara']

    # Delete file
    manager.delete_contacts()
    
def path_test():
    manager = data_manager.PathManager()

    # Pfad speichern
    manager.save_path({
        "ExportDir": "C:/Users/Admin/Documents/Exports",
        "Logs": "C:/Users/Admin/Documents/Logs"
    })

    # Alle geladenen Pfade anzeigen
    print(manager.load_paths())
    # → {'ExportDir': 'C:/Users/Admin/Documents/Exports', 'Logs': 'C:/Users/Admin/Documents/Logs'}

    # Einen bestimmten Pfad abrufen
    print(manager.get_path("Logs"))
    # → 'C:/Users/Admin/Documents/Logs'

    # Datei löschen
    manager.delete_paths()
    
    
def datalogging():
    log = data_manager.EmployeeTaskLogManager()
    log.reset_log()






if __name__=="__main__":
    main()