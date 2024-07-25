from datetime import datetime, timedelta
from enum import Enum
import util, cal


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
    
    def update_status(self, new_status):
        if new_status == 'c':
            self.status = Status.COMPLETE
        elif new_status == 's':
            self.status = Status.STARTED
        elif new_status == 'o':
            self.status = Status.OPEN
        else:
            raise ValueError("Parameter does not represent a class Status object")


def pull_recurring_items(file_location: str) -> list:
    """
    Takes as input a file location (str) and imports data from the text file into a list of TODO
    class objects, returning the list.
    """
    todo_list = []

    with open(file_location) as file:
        for row, line in enumerate(file.readlines()):
            if  row > 1 and line != "\n": # To ignore the header and the EOF character
                stat_str = line[3:11].strip()
                if stat_str == "open":
                    stat = Status.OPEN
                elif stat_str == "started":
                    stat = Status.STARTED
                elif stat_str == "complete":
                    stat = Status.COMPLETE
                else:
                    stat = Status.OPEN

                todo_list.append(TODO(int(line[0:2]), stat, line[12:20].strip(),
                                      line[21:57].strip()))
    # Assign id
    for i, todo in enumerate(todo_list):
        todo.id = i + 1
    return todo_list

def write_data(todo_list: list, month_end:datetime):
    file_location = "data/todo-data.txt"
    with open(file_location, mode="w", encoding="utf-8") as file:
        file.write(f"<eom>\n{month_end.strftime('%x')}\n</eom>\n")
    with open(file_location, mode="a", encoding="utf-8") as file:
        for item in todo_list:
            file.write(f"<record>\n")
            file.write(f"{item.work_day}\n")
            file.write(f"{item.status}\n")
            file.write(f"{item.owner}\n")
            file.write(f"{item.task}\n")
            file.write(f"{item.date.strftime('%x')}\n")
            file.write(f"{item.id}\n")
            file.write(f"</record>\n")
            
def read_data(month_end):
    file_location = "data/todo-data.txt"
    with open(file_location, mode="r", encoding="utf-8") as file:
        is_eom = False
        is_record_part = False
        this_record = []
        todo_list = []
        for line in file.readlines():
            if line == "\n":
                continue
            if line == "<eom>\n":
               is_eom = True
               continue
            if line == "<record>\n":
                is_record_part = True
                continue
            if is_eom:
                item_date = datetime.strptime(line.strip(), "%x")
                if item_date != month_end:
                    raise Exception(f"TODO data file is for Close: {item_date.strftime('%b %Y')}\n"
                                   f"Current Close: {month_end.strftime('%b %Y')}"
                                    )
                else:
                    is_eom = False
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
    end_date = datetime(beg_date.year, beg_date.month + 1, 1) - timedelta(1)
    working_day_table = {}
    # OPEN_ITEM: Consider making this a parameter if the holiday table will be used more than once
    holiday_table = util.pull_holidays("data/holidays.txt")

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


def update_status(todo_list:list, status):
    display_list = util.get_list_segments(todo_list, status)
    if display_list:
        display_list_len = len(display_list)
        sub_list_num = 0
        while True:
            util.clear_screen()
            util.print_display_list(display_list[sub_list_num])
            choice = input("\n (P)revious, (N)ext, (D)one, or Select Item: ").lower()
            if choice == "d":
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
                            print(f"  ID  WD  Date     Day  Status   Owner   Task\n {'-' * 78}\n"
                                    f"{todo.id:>4}{todo.work_day:>4}  "
                                    f"{datetime.strftime(todo.date, '%m/%d/%y %a')}"
                                    f"  {todo.status.value:<8} {todo.owner:<7} {todo.task}")
                            confirm = input("\nUpdate this item? (Y/n) ").lower() or 'y'
                            if confirm == 'y' or confirm == "yes":
                                todo_list[i].update_status('c')
                                display_list = util.get_list_segments(todo_list, status)
                            break
                else:
                    input(f"\nSelection is out of range. Please select again... ")


def display_weekly_calendar(todo_list: list, accounting_period: datetime):
    """
    Prints a report in a weekly calendar view based on a given list of TODO objects, and an
    accounting period date.
    """

    # Get a list of the start of each week in the given month
    todo_month = datetime(accounting_period.year, accounting_period.month + 1, 1)
    first_monday = cal.calc_first_monday(todo_month)
    weeks = cal.calc_calendar_weeks(first_monday)

    util.clear_screen() 
    for week in weeks:

        # Populate the weely calendar with todo items and holidays
        test_matrix = util.pivot_week_items(todo_list, weeks[week])
        util.draw_week(weeks[week])
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
        
    input("...")

    
def simple_report(todo_list: list, status:list):
    """
    Prints a simple report filtered on 'status'
    """
    owner_list = util.get_all_owners(todo_list)
    status_len = len(status)

    util.clear_screen()
    print(f"Wd Date     Day Status   Owner   Task")
    print("---------------------------------------------------------------------")
    for i, owner in enumerate(owner_list):
        if i > 0:
            print()
        for todo in todo_list:
            report_str = (f"{todo.work_day:>2} {datetime.strftime(todo.date, '%m/%d/%y %a')} "
                f"{todo.status.value:<8} {todo.owner:<7} {todo.task}")
            if "all" in status and todo.owner == owner:
                print(report_str)
            elif status_len == 1: 
                if "open" in status:
                    if todo.status == Status.OPEN and todo.owner == owner:
                        print(report_str)
                elif "started" in status:
                    if todo.status == Status.STARTED and todo.owner == owner:
                        print(report_str)
                elif "complete" in status:
                    if todo.status == Status.COMPLETE and todo.owner == owner:
                        print(report_str)
                else:
                    if todo.owner == owner:
                        print(report_str)
            elif "open" in status and "started" in status:
                if ((todo.status == Status.OPEN or todo.status == Status.STARTED)
                        and todo.owner == owner):
                    print(report_str)
            elif "open" in status and "complete" in status:
                if ((todo.status == Status.OPEN or todo.status == Status.COMPLETE)
                        and todo.owner == owner):
                    print(report_str)
            elif "started" in status and "complete" in status:
                if ((todo.status == Status.STARTED or todo.status == Status.COMPLETE)
                    and todo.owner == owner):
                    print(report_str)
            else:
                if todo.owner == owner:
                    print(report_str)
    input("...")

