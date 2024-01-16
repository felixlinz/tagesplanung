import csv

def create_daily_hours_file(filename="daily_hours.csv"):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours = "08:00"  # 8 hours

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for day in days:
            writer.writerow([day, hours])

create_daily_hours_file()