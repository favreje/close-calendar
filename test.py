from datetime import datetime, timedelta
from cal_functs import *

test_date = datetime(2024, 6, 30)
test_result = get_first_monday(test_date)
test_result_string = test_result.strftime("%a %m/%d/%Y")
test_date_string = test_date.strftime("%a %m/%d/%Y")
week_start = get_calendar_weeks(get_first_monday(test_date))


def test_full_year():  
    print("--- Begin test data for test_full_year ---")
    for i in range(12):
        this_date = get_first_monday(datetime(2024, i + 1, 25))
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
