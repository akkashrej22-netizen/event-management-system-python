import os
import datetime

DATA_FILE = "events.txt"
BACKUP_FILE = "events_backup.txt"

events = []



# FILE HANDLING

def load_data():
    global events
    events = []

    if not os.path.exists(DATA_FILE):
        print("No previous schedule found. Starting fresh.")
        return

    try:
        file = open(DATA_FILE, "r")
    except OSError:
        print("Warning: could not open data file. Starting fresh.")
        return

    try:
        while True:
            name = file.readline()
            if name == "":
                break  
            name = name.rstrip('\n')

            date = file.readline().rstrip('\n')
            start_time = file.readline().rstrip('\n')
            end_time = file.readline().rstrip('\n')
            location = file.readline().rstrip('\n')
            description = file.readline().rstrip('\n')
            attendees_str = file.readline().rstrip('\n')

            if attendees_str == "":
                attendees_list = []
            else:
                attendees_list = attendees_str.split(",")

            event = {
                "name": name,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "location": location,
                "description": description,
                "attendees": attendees_list
            }
            events.append(event)
    except Exception:
        print("Warning: data file appears corrupted. Loaded what was readable.")
    finally:
        file.close()


def save_data():
    if os.path.exists(DATA_FILE):
        try:
            backup = open(BACKUP_FILE, "w")
            original = open(DATA_FILE, "r")
            backup.write(original.read())
            original.close()
            backup.close()
        except OSError:
            print("Warning: could not create backup file.")

    try:
        file = open(DATA_FILE, "w")
    except OSError:
        print("Error: could not save data. Changes may be lost.")
        return

    for event in events:
        file.write(event["name"] + "\n")
        file.write(event["date"] + "\n")
        file.write(event["start_time"] + "\n")
        file.write(event["end_time"] + "\n")
        file.write(event["location"] + "\n")
        file.write(event["description"] + "\n")
        attendees_str = ",".join(event["attendees"])
        file.write(attendees_str + "\n")
    file.close()



# VALIDATION CHECKS

def validate_date(date):
    if date == "" or date.isspace():
        print("Error: Date cannot be empty.")
        return False

    if len(date) != 10:
        print("Error: Date must be in DD/MM/YYYY format.")
        return False

    if date[2] != "/" or date[5] != "/":
        print("Error: Date must use '/' as separator.")
        return False

    day_part = date[0:2]
    month_part = date[3:5]
    year_part = date[6:10]

    if not (day_part.isdigit() and month_part.isdigit() and year_part.isdigit()):
        print("Error: Date must contain numbers only.")
        return False

    day = int(day_part)
    month = int(month_part)
    year = int(year_part)

    try:
        datetime.date(year, month, day)
    except ValueError:
        print("Error: That is not a real calendar date.")
        return False

    return True


def validate_time(time):
    if time == "" or time.isspace():
        print("Error: Time cannot be empty.")
        return False

    if len(time) != 5:
        print("Error: Time must be in HH:MM format.")
        return False

    if time[2] != ":":
        print("Error: Time must use ':' as separator.")
        return False

    hour_part = time[0:2]
    minute_part = time[3:5]

    if not (hour_part.isdigit() and minute_part.isdigit()):
        print("Error: Time must contain numbers only.")
        return False

    hour = int(hour_part)
    minute = int(minute_part)

    if hour < 0 or hour > 23:
        print("Error: Hour must be between 00 and 23.")
        return False

    if minute < 0 or minute > 59:
        print("Error: Minutes must be between 00 and 59.")
        return False

    return True


def time_to_minutes(time):
    hour = int(time[:2])
    minute = int(time[3:])
    return hour * 60 + minute


def check_clash(date, start_time, end_time, location, ignore_event=None):

    new_start = time_to_minutes(start_time)
    new_end = time_to_minutes(end_time)

    for event in events:

        if event is ignore_event:
            continue

        if event["date"] == date and event["location"] == location:

            existing_start = time_to_minutes(event["start_time"])
            existing_end = time_to_minutes(event["end_time"])

            if new_start < existing_end and new_end > existing_start:
                return True

    return False

def is_date_in_past(date):
    day = int(date[0:2])
    month = int(date[3:5])
    year = int(date[6:10])
    entered_date = datetime.date(year, month, day)
    return entered_date < datetime.date.today()


def is_datetime_in_past(date, time):
    day = int(date[0:2])
    month = int(date[3:5])
    year = int(date[6:10])
    hour = int(time[0:2])
    minute = int(time[3:5])
    entered_moment = datetime.datetime(year, month, day, hour, minute)
    return entered_moment < datetime.datetime.now()


def name_exists(name, ignore_event=None):
    for event in events:
        if event is ignore_event:
            continue
        if event["name"].strip().lower() == name.strip().lower():
            return True
    return False


def find_event_by_name(name):
    for event in events:
        if event["name"].strip().lower() == name.strip().lower():
            return event
    return None


def date_sort_key(event):
    try:
        day = int(event["date"][0:2])
        month = int(event["date"][3:5])
        year = int(event["date"][6:10])
        hour = int(event["start_time"][0:2])
        minute = int(event["start_time"][3:5])
        return (year, month, day, hour, minute)
    except (ValueError, IndexError):
        return (9999, 12, 31, 23, 59)



# MAIN PROGRAM

def add_event():
    print("\n" + "=" * 50)
    print("CREATE NEW EVENT")
    print("=" * 50)

   
    while True:
        name = input("Enter event name: ")
        if name == "" or name.isspace():
            print("Error: Event name cannot be empty.")
        elif name_exists(name):
            print("Error: An event with this name already exists. Choose a different name.")
        else:
            break

   
    while True:
        date = input("Enter date (DD/MM/YYYY): ")
        if not validate_date(date):
            continue
        if is_date_in_past(date):
            print("Error: Date cannot be in the past. Enter today or a future date.")
            continue
        break

   
    while True:

        start_time = input("Enter start time (HH:MM): ")

        if not validate_time(start_time):
            continue

        end_time = input("Enter end time (HH:MM): ")

        if not validate_time(end_time):
            continue

        if time_to_minutes(end_time) <= time_to_minutes(start_time):
            print("Error: End time must be after start time.")
            continue

        if is_datetime_in_past(date, start_time):
            print("Error: Event start time has already passed.")
            continue

        location = input("Enter location: ")

        if location == "" or location.isspace():
            print("Error: Location cannot be empty.")
            continue

        if check_clash(date,start_time,end_time,location):
            print("Error: Venue is already booked during this time.")
            continue

        break

    description = input("Enter description: ")

    event = {
        "name": name,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "location": location,
        "description": description,
        "attendees": []
    }

    events.append(event)
    save_data()
    print("\nEvent '" + name + "' added successfully!")


def update_event():
    print("\n" + "=" * 50)
    print("MODIFY EVENT")
    print("=" * 50)

    if len(events) == 0:
        print("No events to update.")
        return

    for event in events:
        print("- " + event["name"])

    while True:
        name = input("\nEnter event name to update: ")
        if name == "" or name.isspace():
            print("Error: Event name cannot be empty.")
        else:
            break

    event = find_event_by_name(name)
    if event is None:
        print("Event not found!")
        return

    while True:
        print("\nWhat would you like to update for '" + event["name"] + "'?")
        print("1 - Date")
        print("2 - Time")
        print("3 - Location")
        print("4 - Description")
        print("5 - Done updating")

        choice = input("Enter choice (1-5): ")

        if choice == "1":
            while True:
                new_date = input("New date (DD/MM/YYYY): ")
                if not validate_date(new_date):
                    continue
                if is_date_in_past(new_date):
                    print("Error: Date cannot be in the past. Enter today or a future date.")
                    continue
                if check_clash(new_date, event["time"], event["location"], ignore_event=event):
                    print("Error: Venue clash! Location is already booked at that new date/time.")
                    continue
                event["date"] = new_date
                print("Date updated!")
                break

        elif choice == "2":
            while True:
                new_start = input("New start time (HH:MM): ")
                new_end = input("New end time (HH:MM): ")
                if not validate_time(new_start):
                    continue
                if not validate_time(new_end):
                    continue
                if time_to_minutes(new_end) <= time_to_minutes(new_start):
                    print("Error: End time must be after start time.")
                    continue
                if check_clash(
                    event["date"],
                    new_start,
                    new_end,
                    event["location"],
                    ignore_event=event
                ):
                    print("Error: Venue clash!")
                    continue

                event["start_time"] = new_start
                event["end_time"] = new_end

                print("Time updated!")
                break

        elif choice == "3":
            while True:
                new_location = input("New location: ")
                if new_location == "" or new_location.isspace():
                    print("Error: Location cannot be empty.")
                    continue
                if check_clash(event["date"], event["time"], new_location, ignore_event=event):
                    print("Error: Venue clash! Location is already booked at this time.")
                    continue
                event["location"] = new_location
                print("Location updated!")
                break

        elif choice == "4":
            while True:
                new_description = input("New description: ")
                if new_description == "" or new_description.isspace():
                    print("Error: Description cannot be empty.")
                else:
                    event["description"] = new_description
                    print("Description updated!")
                    break

        elif choice == "5":
            save_data()
            print("Finished updating event!")
            return

        else:
            print("Invalid choice! Please re-enter.")


def delete_event():
    print("\n" + "=" * 50)
    print("DELETE EVENT")
    print("=" * 50)

    if len(events) == 0:
        print("No events to delete.")
        return

    for event in events:
        print("- " + event["name"])

    while True:
        name = input("\nEnter event name to delete: ")
        if name == "" or name.isspace():
            print("Error: Event name cannot be empty.")
        else:
            break

    event = find_event_by_name(name)
    if event is None:
        print("Event not found!")
        return

    confirm = input("Are you sure you want to delete '" + event["name"] + "'? (Y/N): ")
    if confirm.upper() == "Y":
        events.remove(event)
        save_data()
        print("Event deleted successfully!")
    else:
        print("Deletion cancelled.")


def search_events():
    print("\n" + "=" * 50)
    print("SEARCH EVENTS")
    print("=" * 50)

    if len(events) == 0:
        print("No events available.")
        return

    keyword = input("Enter keyword (searches name, location, description): ").strip().lower()
    if keyword == "":
        print("Error: Search keyword cannot be empty.")
        return

    matches = []
    for event in events:
        if (keyword in event["name"].lower()
                or keyword in event["location"].lower()
                or keyword in event["description"].lower()):
            matches.append(event)

    if len(matches) == 0:
        print("No events matched '" + keyword + "'.")
        return

    matches.sort(key=date_sort_key)
    print("\nFound " + str(len(matches)) + " matching event(s):")
    for event in matches:
        print_event(event)


def manage_attendees():
    print("\n" + "=" * 50)
    print("MANAGE ATTENDEES")
    print("=" * 50)

    if len(events) == 0:
        print("No events available.")
        return

    for event in events:
        print("- " + event["name"])

    while True:
        name = input("\nEnter event name: ")
        if name == "" or name.isspace():
            print("Error: Event name cannot be empty.")
        else:
            break

    event = find_event_by_name(name)
    if event is None:
        print("Event not found!")
        return

    print("\nCurrent attendees: " + (", ".join(event["attendees"]) if event["attendees"] else "None"))
    print("1 - Add Attendee")
    print("2 - Update Attendee")
    print("3 - Delete Attendee")
    choice = input("Enter choice: ")

    if choice == "1":
        attendee = input("Enter attendee name: ").strip()
        if attendee == "":
            print("Error: Attendee name cannot be empty.")
        elif attendee in event["attendees"]:
            print("Error: This attendee is already on the list.")
        else:
            event["attendees"].append(attendee)
            save_data()
            print("Attendee added!")

    elif choice == "2":
        old = input("Enter attendee name to update: ").strip()
        if old in event["attendees"]:
            new = input("Enter new name: ").strip()
            if new == "":
                print("Error: New name cannot be empty.")
            else:
                index = event["attendees"].index(old)
                event["attendees"][index] = new
                save_data()
                print("Attendee updated!")
        else:
            print("Attendee not found!")

    elif choice == "3":
        attendee = input("Enter attendee name to delete: ").strip()
        if attendee in event["attendees"]:
            event["attendees"].remove(attendee)
            save_data()
            print("Attendee deleted!")
        else:
            print("Attendee not found!")

    else:
        print("Invalid choice!")


def print_event(event):
    """Print a single event in a clean, professional layout."""
    print("\n" + "-" * 48)
    print("Event Name : " + event["name"])
    print("Date       : " + event["date"])
    print("Time       : " + event["start_time"] + " - " + event["end_time"])
    print("Location   : " + event["location"])
    print("Description: " + event["description"])
    if event["attendees"]:
        print("Attendees  : " + ", ".join(event["attendees"]) + " (" + str(len(event["attendees"])) + " total)")
    else:
        print("Attendees  : None")
    print("-" * 48)


def display_schedule():
    print("\n" + "=" * 50)
    print("CURRENT SCHEDULE")
    print("=" * 50)

    if len(events) == 0:
        print("No events available.")
        return

    sorted_events = sorted(events, key=date_sort_key)
    for event in sorted_events:
        print_event(event)


def display_report():
    """A simple summary report of the current schedule."""
    print("\n" + "=" * 50)
    print("SCHEDULE REPORT")
    print("=" * 50)

    if len(events) == 0:
        print("No events available.")
        return

    total = len(events)
    total_attendees = 0
    location_counts = {}

    for event in events:
        total_attendees += len(event["attendees"])
        loc = event["location"]
        location_counts[loc] = location_counts.get(loc, 0) + 1

    busiest_location = max(location_counts, key=location_counts.get)

    print("Total Events        : " + str(total))
    print("Total Attendees     : " + str(total_attendees))
    print("Most-Used Location  : " + busiest_location + " (" + str(location_counts[busiest_location]) + " event(s))")



# MAIN MENU

def main():
    load_data()

    while True:
        print("\n" + "=" * 35)
        print("      EVENT MANAGEMENT SYSTEM")
        print("=" * 35)
        print("1 - Create New Event")
        print("2 - View Schedule")
        print("3 - Search Events")
        print("4 - Modify Event")
        print("5 - Delete Event")
        print("6 - Manage Attendees")
        print("7 - View Report")
        print("8 - Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_event()
        elif choice == "2":
            display_schedule()
        elif choice == "3":
            search_events()
        elif choice == "4":
            update_event()
        elif choice == "5":
            delete_event()
        elif choice == "6":
            manage_attendees()
        elif choice == "7":
            display_report()
        elif choice == "8":
            save_data()
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number from 1-8.")


if __name__ == "__main__":
    main()
