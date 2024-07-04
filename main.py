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
    test_week = datetime(2024, 7, 15)
    SPACER = 19 * " "
    print(f"{SPACER}Mon{(SPACER * 2)}  Tue{SPACER * 2}  Wed{SPACER * 2}  Thu{SPACER * 2}  Fri")
    test_matrix = util.pivot_week_items(todo_list, test_week)
    util.draw_week(test_week)
    for i, row in enumerate(test_matrix):
        if i != 0:
            print()
        for i in row:
            if i is not None:
                if i.status == Status.OPEN:
                    print(" [.] ", end="")
                elif i.status == Status.STARTED:
                    print(" [S] ", end="")
                elif i.status == Status.COMPLETE:
                    print(" [x] ", end="")
                print(f"{i.task}{(38 - len(i.task)) * ' '}", end="")
            else:
                print(f"{43 * ' '}", end="")
    print("\n")

if __name__ == "__main__":
    main()

