from datetime import datetime, timedelta

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





