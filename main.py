from datetime import datetime, timedelta
from main_func import *
import front_end as fe
import test
import util

def main():
    accounting_period = datetime(2024, 6, 30)
    # todo_file_location = "data/close.txt"
    # todo_list = pull_recurring_items(todo_file_location) # refactor: change name to pull_recurring_items()
    # todo_list = assign_date(todo_list, accounting_period)
    # simple_report(todo_list, ["open", "started"])
    # display_weekly_calendar(todo_list, accounting_period)

    # write_data(todo_list, accounting_period)
    working_list = read_data(accounting_period)
    # simple_report(working_list, ["all"])




    fe.main()

if __name__ == "__main__":
    main()

