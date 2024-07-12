from datetime import datetime, timedelta
from main_func import *
import front_end as fe
import test
import util

def main():
    accounting_period = datetime(2024, 6, 30)
    todo_file_location = "data/close.txt"
    todo_list = pull_recurring_items(todo_file_location) # refactor: change name to pull_recurring_items()
    todo_list = assign_date(todo_list, accounting_period)
    # simple_report(todo_list, ["open", "started"])
    # display_weekly_calendar(todo_list, accounting_period)

    write_data(todo_list, accounting_period)
    working_list = read_data(accounting_period)
    # simple_report(working_list, ["all"])

    # --- Testing updated read_data() and write_data() to incorporate self.id class attribute
    for todo in working_list:
        if todo.id == 38:
            todo.status = Status.COMPLETE
        if todo.id == 60:
            todo.owner = "Thor"
            todo.task = "Arm wrestle Hercules"
        if todo.id == 59:
            todo.status = Status.STARTED
            todo.owner = "Sisyphus"
            todo.task = "Roll the bolder back up the hill (again)"

    for todo in working_list:
        print(f"{todo.id:>2} {todo.status.value:<10} {todo.owner:<8} {todo.task}")

    write_data(working_list, accounting_period)

    # fe.menu_loop()

if __name__ == "__main__":
    main()

