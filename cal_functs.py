from datetime import datetime, timedelta


SPACING = " " * 17
UNDERLINE = "-" * 214

# length of date + spacing on each end - indentation on each end
CELL_WIDTH = 6 + (len(SPACING) * 2) 


def get_first_monday(in_date: datetime) -> datetime:
    """
    Takes 'year' (int) and 'month' (int) as input and returns
    the first Monday of that month (datetime)
    """
    d = datetime(in_date.year, in_date.month, 1)
    if d.weekday() == 0:
        return d
    offset = 7 - d.weekday()
    return d + timedelta(offset)


def get_calendar_weeks(first_monday: datetime) -> dict:
    """
    Takes the first day of a given month (datetime) as input and returns a dict of the first Monday
    for each of the consecutive six week periods beginning with the first day of the month
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


def pull_todo_items(path):
    # Import items from a text file and save to a list of dicts. Fields will include:
    # Workday, Status, Owner, Process
    pass

def assign_date(workday_num: int) -> datetime:
    # Will have as a dependency a table of holidays and the respective date. This will be a
    # separate function that will retrieve holidays from a text file and store as a dict for
    # reference. Holidays are ignored for purposes of calculating assigning work days to dates.
    pass



