from datetime import datetime, timedelta
from enum import Enum


SPACING = " " * 17
UNDERLINE = "-" * 214

# length of date + spacing on each end - indentation on each end
CELL_WIDTH = 6 + (len(SPACING) * 2) 


class Status(Enum):
    OPEN = "open"
    STARTED = "started"
    COMPLETE = "complete"


class TODO:
    def __init__(self, work_day: int, status: Status, owner: str, task: str):
        self.work_day = work_day
        self.status = status
        self.owner = owner
        self.task = task
        self.date: datetime | None = None

    def __repr__(self) -> str:
            return (
                f"TODO(work_day={self.work_day}, status='{self.status.value}', "
                f"owner='{self.owner}', task='{self.task}', task_date='{self.date}')"
            )


def calc_first_monday(in_date: datetime) -> datetime:
    """
    Takes 'year' (int) and 'month' (int) as input and returns
    the first Monday of that month (datetime)
    """
    d = datetime(in_date.year, in_date.month, 1)
    if d.weekday() == 0:
        return d
    offset = 7 - d.weekday()
    return d + timedelta(offset)


def calc_calendar_weeks(first_monday: datetime) -> dict:
    """
    Takes the first Monday day of a given month (datetime) as input and returns a dict of the first
    Monday for each of the consecutive six week periods beginning with the first day of the month
    """
    week_start = {}

    if first_monday.day == 1:
        initial_week = first_monday
    else:
        initial_week = first_monday - timedelta(7)
    week_start["week1"] = initial_week
    week_start["week2"] = week_start["week1"] + timedelta(7)
    week_start["week3"] = week_start["week2"] + timedelta(7)
    week_start["week4"] = week_start["week3"] + timedelta(7)
    week_start["week5"] = week_start["week4"] + timedelta(7)
    week_start["week6"] = week_start["week5"] + timedelta(7)
    return week_start


def draw_week(first_monday: datetime):
    """
    Takes a datetime representing the first Monday for one of six weeks and draws the calendar
    header for that  particular week
    """
    print()
    for offset in range(5):
        d = (first_monday + timedelta(offset)).strftime("%b-%d")
        print(f"[{SPACING}{d}{SPACING}]", end = " ")
    print("\n" + UNDERLINE)


def pull_holidays(file_location: str) -> dict:
    """
    Reads text data from 'file_location' and returns a dict with key (datetime) representing the
    holiday date and value (str) representing the holiday description.
    """
    holiday_dict = {}
    with open(file_location) as file:
        for line in file.readlines():
            parsed_line = line.split(",")
            date_part = datetime.strptime(parsed_line[0], "%m/%d/%y")
            desc_part = parsed_line[1].strip()
            holiday_dict[date_part] = desc_part
        return holiday_dict 


def pull_todo_items(file_location: str) -> list:
    """
    Takes as input a file location (str) and imports data from the text file into a list of TODO
    class objects, returning the list.
    """
    todo_list = []

    with open(file_location) as file:
        for row, line in enumerate(file.readlines()):
            if  row > 1 and line != "\n": # To ignore the header and the EOF character
                stat_str = line[3:11].strip()
                if stat_str == "open":
                    stat = Status.OPEN
                elif stat_str == "started":
                    stat = Status.STARTED
                elif stat_str == "complete":
                    stat = Status.COMPLETE
                else:
                    stat = Status.OPEN

                todo_list.append(TODO(int(line[0:2]), stat, line[12:20].strip(),
                                      line[21:57].strip()))
    return todo_list


def assign_date(todo_list: list, close_month: datetime) -> list:
    # Iterate over each date in the month and assign working days to the respective date. Then
    # populate todo list items with the date that corresponds to it's working day.
    beg_date = close_month + timedelta(1)
    end_date = datetime(beg_date.year, beg_date.month + 1, 1) - timedelta(1)
    working_day_table = {}
    # OPEN_ITEM: Consider making this a parameter if the holiday table will be used more than once
    holiday_table = pull_holidays("data/holidays.txt")

    # Populate the working_day_table with corresponding dates
    current_working_day = 1
    for d in range(beg_date.day, end_date.day + 1):
        this_date = datetime(beg_date.year, beg_date.month, d)
        if this_date in holiday_table:
            continue
        if this_date.weekday() > 4: 
            continue
        working_day_table[current_working_day] = this_date
        current_working_day += 1

    # Populate the todo list items with dates that correspond to the item's working day

    # OPEN_ITEM: Need to make sure working day per the source text file constrained to only those
    # within the working_day_table range. (e.g. a working day of 35 in the text file will throw a
    # KeyError)

    for todo in todo_list:
        if todo.work_day in working_day_table:
            todo.date = working_day_table[todo.work_day]
        else:
            # Need something more elegant. Consider whether we want to constrain the working days
            # to only the subsequent month for the close period (and throw an exception here), or
            # lengthen the close period - maybe 90 days? - and only throw an exception if outside
            # of that range. But in either case, not a date of 01/01/01. 
            todo.date = datetime(1,1,1) 
    return todo_list


def update_todo_text_file(path):
    # function to write modifications to fields in the text file when called
    pass

def display_weekly_calendar():
    # Populate the weely calendar with todo items and holidays
    pass
