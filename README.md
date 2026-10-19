EVENT MANAGEMENT SYSTEM
=======================

A command-line Python program for creating and managing an event schedule.

FEATURES
--------
- Create events with a name, date, start and end time, location, and description.
- View all events in chronological order.
- Search events by name, location, or description.
- Modify an event's date, time, location, or description.
- Delete events with a confirmation prompt.
- Add, update, and remove attendees for an event.
- View a schedule report with total events, total attendees, and the most-used location.
- Prevent duplicate event names and overlapping bookings at the same location.
- Validate dates (DD/MM/YYYY), times (HH:MM), empty inputs, and past event dates/times.
- Save event data automatically between sessions.

REQUIREMENTS
------------
- Python 3
- No third-party packages are required.

HOW TO RUN
----------
1. Open a terminal in this project folder.
2. Run:

   python Main.py

3. Select an option from the menu by entering a number from 1 to 8.

MENU OPTIONS
------------
1 - Create New Event
2 - View Schedule
3 - Search Events
4 - Modify Event
5 - Delete Event
6 - Manage Attendees
7 - View Report
8 - Exit

DATE AND TIME FORMATS
---------------------
- Date: DD/MM/YYYY (example: 25/12/2026)
- Time: HH:MM in 24-hour time (example: 14:30)

DATA STORAGE
------------
The program creates the following files in the folder where it is run:

- events.txt: stores the current event schedule.
- events_backup.txt: stores a backup of the previous schedule before saving changes.

Keep these files with Main.py if you want to retain your saved events. If no
events.txt file exists, the program starts with an empty schedule.

NOTES
-----
- Event names must be unique, ignoring letter case.
- A location cannot be booked for two events whose times overlap on the same date.
- Event dates must be today or later, and event start times cannot already have passed.\
