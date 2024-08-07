from datetime import datetime, timedelta
from enum import Enum
import util, cal
import sys


class Status(Enum):
    OPEN = "open"
    STARTED = "started"
    COMPLETE = "complete"


class TODO:
    def __init__(self, work_day: int, status: Status, owner: str, task: str):
        self.work_day = work_day
        self.status = status
        self.owner = owner
        self.task = task
        self.date: datetime | None = None
        self.id: int | None = None

    def __repr__(self) -> str:
            return (
                f"TODO(work_day={self.work_day}, status='{self.status.value}', "
                f"owner='{self.owner}', task='{self.task}', task_date='{self.date}', id={self.id})"
            )
    

def pull_recurring_items(file_location: str) -> list:
    """
    Takes as input a file location (str) and imports data from the text file into a list of TODO
    class objects, returning the list.
    """
    todo_list = []
    status = Status.OPEN

    with open(file_location) as file:
        for row, line in enumerate(file.readlines()):
            if row > 1 and line != "\n": # To ignore header and any blank lines
                work_day = int(line[0:2])
                owner = line[3:11].strip()
                task = line[12:45].strip()
                id = row - 1
                this_todo = TODO(work_day, status, owner, task)
                this_todo.id = id
                todo_list.append(this_todo)

    return todo_list




def write_data(todo_list: list):
    file_location = "data/working-list.dat"
    with open(file_location, mode="w", encoding="utf-8") as file:
        for item in todo_list:
            file.write(f"<record>\n")
            file.write(f"{item.work_day}\n")
            file.write(f"{item.status}\n")
            file.write(f"{item.owner}\n")
            file.write(f"{item.task}\n")
            file.write(f"{item.date.strftime('%x')}\n")
            file.write(f"{item.id}\n")
            file.write(f"</record>\n")
            
def read_data():
    file_location = "data/working-list.dat"
    with open(file_location, mode="r", encoding="utf-8") as file:
        is_record_part = False
        this_record = []
        todo_list = []
        for line in file.readlines():
            if line == "\n":
                continue
            if line == "<record>\n":
                is_record_part = True
                continue
            if is_record_part:
                this_record.append(line.strip())
            if line == "</record>\n":
                work_day = int(this_record[0])
                member_name = this_record[1].split(".")[-1]
                status = Status[member_name]
                owner = this_record[2]
                task = this_record[3]
                this_todo = TODO( work_day, status, owner, task)
                this_todo.date = datetime.strptime(this_record[4], "%x")
                this_todo.id = int(this_record[5])
                todo_list.append(this_todo)
                this_record = []
                is_record_part = False
    return todo_list
    

def assign_date(todo_list: list, close_month: datetime) -> list:
    # Iterate over each date in the month and assign dates based on working days.
    beg_date = close_month + timedelta(1)
    end_date = cal.eom(beg_date)
    working_day_table = {}
    # OPEN_ITEM: Consider making this a parameter if the holiday table will be used more than once
    holiday_table = util.pull_holidays()

    # Populate the working_day_table with corresponding dates
    current_working_day = 1
    for d in range(beg_date.day, end_date.day + 1):
        this_date = datetime(beg_date.year, beg_date.month, d)
        if this_date in holiday_table:
            continue
        if this_date.weekday() > 4: 
            continue
        working_day_table[current_working_day] = this_date
        current_working_day += 1

    # Populate the todo list items with dates that correspond to the item's working day

    # OPEN_ITEM: Need to make sure working day per the source text file constrained to only those
    # within the working_day_table range. (e.g. a working day of 35 in the text file will throw a
    # KeyError)

    for todo in todo_list:
        if todo.work_day in working_day_table:
            todo.date = working_day_table[todo.work_day]
        else:
            # Need something more elegant. Consider whether we want to constrain the working days
            # to only the subsequent month for the close period (and throw an exception here), or
            # lengthen the close period - maybe 90 days? - and only throw an exception if outside
            # of that range. But in either case, not a date of 01/01/01. 
            todo.date = datetime(1,1,1) 
    return todo_list


def update_status(todo_list: list, current_status: list, new_status: Status):
    splash = f"\n{' ' * 12}=============== UPDATE COMPLETION STATUS =============== \n\n"
    was_modified = False
    display_list = util.get_list_segments(todo_list, current_status)
    if display_list:
        display_list_len = len(display_list)
        sub_list_num = 0
        while True:
            util.clear_screen()
            util.print_display_list(display_list[sub_list_num], splash)
            choice = input("\n (P)revious, (N)ext, (D)one, or Select Item: ").lower()
            if choice == "d":
                if was_modified:
                    write_data(todo_list)
                break
            elif choice == "p":
                if sub_list_num > 0:
                    sub_list_num -= 1
                util.clear_screen()
            elif choice == "n":
                if sub_list_num < display_list_len - 1:
                    sub_list_num += 1
                util.clear_screen()
            elif choice.isnumeric():
                available_to_select = [i.id for i in display_list[sub_list_num]]
                sel_num = int(choice)
                if sel_num in available_to_select:
                    # Get and confirm choice before updating
                    for i, todo in enumerate(todo_list):
                        if todo.id == sel_num:
                            print(f"\n  ID  WD  Date     Day  Status   Owner   Task\n {'-' * 78}\n"
                                    f"{todo.id:>4}{todo.work_day:>4}  "
                                    f"{datetime.strftime(todo.date, '%m/%d/%y %a')}"
                                    f"  {todo.status.value:<8} {todo.owner:<7} {todo.task}")
                            confirm = input("\nUpdate this item? (Y/n) ").lower() or 'y'
                            if confirm == 'y' or confirm == "yes":
                                todo_list[i].status = new_status
                                was_modified = True
                                new_display_list = util.get_list_segments(todo_list, current_status)
                                if new_display_list:
                                    display_list = new_display_list
                            break
                else:
                    input(f"\nSelection is out of range. Please select again... ")
    else:
        print(f"\nNo items met your criteria. Press 'Enter' to return to the Menu.")
        input("---")


def change_due_date(todo_list: list):
    splash = f"\n{' ' * 6}{'=' * 25} UPDATE DUE DATE {'=' * 25}\n\n"
    was_modified = False
    all = [Status.OPEN, Status.STARTED, Status.COMPLETE]
    wd_table = util.working_days_table()
    display_list = util.get_list_segments(todo_list, all)
    if display_list:
        display_list_len = len(display_list)
        sub_list_num = 0
        while True:
            util.clear_screen()
            util.print_display_list(display_list[sub_list_num], splash)
            choice = input("\n (P)revious, (N)ext, (D)one, or Select Item: ").lower()
            if choice == "d":
                if was_modified:
                    write_data(todo_list)
                break
            elif choice == "p":
                if sub_list_num > 0:
                    sub_list_num -= 1
                util.clear_screen()
            elif choice == "n":
                if sub_list_num < display_list_len - 1:
                    sub_list_num += 1
                util.clear_screen()
            elif choice.isnumeric():
                available_to_select = [i.id for i in display_list[sub_list_num]]
                sel_num = int(choice)
                if sel_num in available_to_select:
                    # Get and confirm choice before updating
                    for i, todo in enumerate(todo_list):
                        if todo.id == sel_num:
                            print(f"\n  ID  WD  Date     Day  Status   Owner   Task\n {'-' * 78}\n"
                                    f"{todo.id:>4}{todo.work_day:>4}  "
                                    f"{datetime.strftime(todo.date, '%m/%d/%y %a')}"
                                    f"  {todo.status.value:<8} {todo.owner:<7} {todo.task}")
                            confirm = input("\nUpdate this item? (Y/n) ").lower() or 'y'
                            if confirm == 'y' or confirm == "yes":
                                modified_date = util.grab_new_date(wd_table)
                                if modified_date:
                                    todo_list[i].date = modified_date[0]
                                    todo_list[i].work_day = modified_date[1]
                                    was_modified = True
                                    display_list = util.get_list_segments(todo_list, all)
                            break
                else:
                    input(f"\nSelection is out of range. Please select again... ")
    else:
        print(f"\nNo items met your criteria. Press 'Enter' to return to the Menu.")
        input("---")


def display_weekly_calendar(todo_list: list, accounting_period: datetime):
    """
    Prints a report in a weekly calendar view based on a given list of TODO objects, and an
    accounting period date.
    """

    # Get a list of the start of each week in the given month
    todo_month = cal.first_of_next_month(accounting_period)
    first_monday = cal.calc_first_monday(todo_month)
    weeks = cal.calc_calendar_weeks(first_monday)

    util.clear_screen() 
    for week in weeks:

        # Populate the weekly calendar with todo items and holidays
        matrix = util.pivot_week_items(todo_list, weeks[week])
        util.draw_week(weeks[week])
        for i, row in enumerate(matrix):
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
        
    input("---")
    

def report_by_day(todo_list: list, status:list):
    """
    Prints a simple report filtered on 'status' grouping by work_day
    """
    filtered_list = sorted([i for i in todo_list if i.status in status], key=lambda i: i.work_day)
    util.clear_screen()
    if not filtered_list:
        input(f"\n\nNo items for this report. Press Enter to return to the Menu.\n---")
        return
    current_day = filtered_list[0].work_day
    print(f"Wd Date     Day Status   Owner   Task")
    print("---------------------------------------------------------------------")
    for item in filtered_list:
        if item.work_day != current_day:
            current_day = item.work_day
            print()
        print(f"{item.work_day:>2} {datetime.strftime(item.date, '%m/%d/%y %a')} "
                f"{item.status.value:<8} {item.owner:<7} {item.task}")
    input("---")


def report_by_owner(todo_list: list, status:list):
    """
    Prints a report filtered on 'status' grouping by owner
    """

    # This will ultimately be pulled from a data table
    owner_order = {
        "Ethan": 1,
        "Rosanne": 2,
        "Jerry": 3,
        "Luis": 4,
        "Jeff": 5,
    }

    filtered_list = sorted([i for i in todo_list if i.status in status],
                           key=lambda i: owner_order[i.owner])
    util.clear_screen()
    if not filtered_list:
        input(f"\n\nNo items for this report. Press Enter to return to the Menu.\n---")
        return
    current_owner = filtered_list[0].owner
    print(f"Wd Date     Day Status   Owner   Task")
    print("---------------------------------------------------------------------")
    for item in filtered_list:
        if item.owner != current_owner:
            current_owner = item.owner
            print()
        print(f"{item.work_day:>2} {datetime.strftime(item.date, '%m/%d/%y %a')} "
                f"{item.status.value:<8} {item.owner:<7} {item.task}")
    input("---")


def init_month_end(accounting_period):
    todo_file_location = "data/recurring-tasks.dat"
    acct_string = accounting_period.strftime("%b '%y").upper()
    width = 43
    util.clear_screen()
    splash_display = f"\n======= INITIALIZE A NEW CLOSE CALENDAR ========\n" 
    splash_ln_2 = f"Current Month-End Close: {acct_string}".center(width)
    print(splash_display, splash_ln_2)
    user_confirm = input(
        f"\n****************************************************************"
        f"\nWARNING: You are about to initialize a new accounting period.\n"
        f"This process will overwrite your existing data file.\n"
        f"****************************************************************"
        f"\n\nPlease confirm that you wish to continue (y/n): "
    ).lower()
    if user_confirm not in ("y", "yes"):
        return None, None 
    print()
    accounting_period = util.get_accounting_period()
    todo_list = pull_recurring_items(todo_file_location) 
    todo_list = assign_date(todo_list, accounting_period)
    write_data(todo_list)
    util.write_accounting_period(accounting_period)
    print(f"\n\nA new Close Calendar for {accounting_period.strftime('%B %Y')} was successfully created.")
    print(f"Please restart the application for the change to take effect.\n")
    input("Press 'Enter' to continue...")
    sys.exit(0)
