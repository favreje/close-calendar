from main_func import *
from datetime import datetime, timedelta
import test
import util

def main():
    accounting_period = datetime(2024, 6, 30)
    todo_file_location = "data/close.txt"
    todo_list = pull_todo_items(todo_file_location)
    todo_list = assign_date(todo_list, accounting_period)
    # simple_report(todo_list, ["open", "started"])

    # Test for pivot_week_items function
    display_weekly_calendar(todo_list, accounting_period)

if __name__ == "__main__":
    main()

