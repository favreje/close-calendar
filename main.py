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
    # display_weekly_calendar(todo_list, accounting_period)

    # Test for read / write
    # write_data(todo_list, accounting_period)
    # new_list = read_data(accounting_period)
    # simple_report(new_list, ["all"])
    for todo in todo_list:
        if todo.id == 38:
            todo.status = Status.COMPLETE
    for todo in todo_list:
        print(f"{todo.id:>2} {todo.status.value} {(10 - len(todo.status.value)) * ' '}{todo.task}")

if __name__ == "__main__":
    main()

