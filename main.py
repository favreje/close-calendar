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
    test_week = util.pivot_week_items(todo_list, datetime(2024, 7, 29))
    for row in test_week:
        print()
        for i in row:
            if i is not None:
                print(f"{i.task}{(40 - len(i.task)) * ' '}", end="")
            else:
                print(f"None{36 * ' '}", end="")
    print()

if __name__ == "__main__":
    main()

