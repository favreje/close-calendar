from datetime import datetime, timedelta
from cal_functs import *

test_date = datetime(2024, 6, 30)
test_date = test_date + timedelta(1)
test_result = calc_first_monday(test_date)
test_result_string = test_result.strftime("%a %m/%d/%Y")
test_date_string = test_date.strftime("%a %m/%d/%Y")
week_start = calc_calendar_weeks(calc_first_monday(test_date))


def test_full_year():  
    print("--- Begin test data for test_full_year ---")
    for i in range(12):
        this_date = calc_first_monday(datetime(2024, i + 1, 25))
        print(f"{i + 1:>5} {this_date.strftime('%a %m/%d/%Y')}")
    print("--- End test data ---\n")


def test_calendar_weeks():
    print("--- Begin test data for test_calendar_weeks ---")
    print(f"The first Monday for the date {test_date_string} is {test_result_string}")
    print()
    for k in week_start:
        dte_str = week_start[k].strftime("%a %m/%d/%Y")
        print(f"Calendar {k} begins with: {dte_str}" )
    print()
    print("--- End test data ---\n")


def test_weekly_display():
    print("--- Begin test data for test_weekly_display ---")
    print()
    for k in week_start:
        draw_week(week_start[k]) 
        print(" Item number 1")
        print()
    print("CELL_WIDTH ", CELL_WIDTH)
    print("--- End test data ---\n")


def test_holiday_import():
    period_end = datetime(2024, 10, 31)
    beg_date = period_end + timedelta(1)
    end_date = datetime(beg_date.year, beg_date.month + 1, 1) - timedelta(1)
    path = "data/holidays.txt"
    hol = pull_holidays(path)
    print("--- Begin test data for test_weekly_display ---")
    print("Complete Holiday List:")
    for k in hol:
        dte_str = datetime.strftime(k, "%x")
        print(dte_str, hol[k])
    print("\nHolidays This Month:")
    print(f"Month End: {datetime.strftime(period_end, '%x')}")
    for k in hol:
        if k >= beg_date and k <= end_date:
            print(datetime.strftime(k, "%x"), hol[k])
    print("--- End test data ---\n")

def test_class_structure():
    todo_item = TODO(1, Status.OPEN, "Ethan", "ARO Accretion")
    print(todo_item)
    todo_item.task_date = datetime(2024, 7, 1)
    print(todo_item)
    todo_item.status = Status.STARTED
    print(todo_item)

def test_pull_todo_items():
    path = "data/close.txt"
    todo_list = pull_todo_items(path)
    print(f"Wd Status   Owner   Task")
    print("---------------------------------------------------------")
    for item in todo_list:
        if item.status == Status.STARTED: 
            print(f"{item.work_day:>2}", end=" ")
            print(f"{item.status.value:<8}", end=" ")
            print(f"{item.owner:<7}", end=" ")
            print(item.task)

