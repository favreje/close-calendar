from main_func import *
from datetime import datetime, timedelta
import test


def main():
    accounting_period = datetime(2024, 12, 31)
    todo_file_location = "data/close.txt"
    todo_list = pull_todo_items(todo_file_location)
    todo_list = assign_date(todo_list, accounting_period)
    simple_report(todo_list, ["open", "started"])


if __name__ == "__main__":
    main()

