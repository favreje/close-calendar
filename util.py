from datetime import datetime, timedelta
import os 
import platform
import cal


SPACING = " " * 15
UNDERLINE = "-" * 214

# length of date + spacing on each end - indentation on each end
CELL_WIDTH = 6 + (len(SPACING) * 2) 


def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def get_all_owners(todo_list):
    owner_list = []
    for todo in todo_list:
        if todo.owner not in owner_list:
            owner_list.append(todo.owner)
    return owner_list


def write_accounting_period(date: datetime):
    """
    Takes a date representing the user's selected accounting period and stores it to a file.
    """
    file_location = "data/accounting-period.dat"
    with open(file_location, mode="w", encoding="utf-8") as file:
        file.write(f"{date.strftime('%x')}\n")


def read_accounting_period() -> datetime:
    """
    Reads the current working accounting period from a data file and returns it.
    """
    file_location = "data/accounting-period.dat"
    with open(file_location, mode="r", encoding="utf-8") as file:
        date_string = file.read().strip()
        return datetime.strptime(date_string, "%x")


def draw_week(first_monday: datetime):
    """
    Takes a datetime representing the first Monday for one of six weeks and draws the calendar
    header for that  particular week
    """
    print()
    for offset in range(5):
        d = (first_monday + timedelta(offset)).strftime("%a %b-%d")
        print(f"[{SPACING}{d}{SPACING}]", end = " ")
    print("\n" + UNDERLINE)


def pull_holidays() -> dict:
    """
    Reads text data from 'file_location' and returns a dict with key (datetime) representing the
    holiday date and value (str) representing the holiday description.
    """
    file_location = "data/holidays.dat"
    holiday_dict = {}
    with open(file_location) as file:
        for line in file.readlines():
            parsed_line = line.split(",")
            date_part = datetime.strptime(parsed_line[0], "%m/%d/%y")
            desc_part = parsed_line[1].strip()
            holiday_dict[date_part] = desc_part
        return holiday_dict 


def pivot_week_items(todo_list: list, first_monday: datetime) -> list:
    """
    Takes a list of TODO objects and a particular week, represented by the first Monday of that
    week and returns a [5 x n] matrix of TODO objects for each weekday in the given week. 
    """
    day_dict = {}

    # Initialize day_dict with empty lists
    for i in range(5):
        day_dict[first_monday + timedelta(i)] = []

    # Create a dict to collect all elements for each 'row'
    for k in day_dict.keys():
        for item in todo_list:
            if k == item.date:
                day_dict[k].append(item)

    # Determine the maximum number of entries for a any 'row'
    max_len = max(len(values) for values in day_dict.values())

    # Create and populate the matrix
    matrix = []
    for i in range(max_len):
        row = []
        for k in sorted(day_dict.keys()):
            if i < len(day_dict[k]):
                row.append(day_dict[k][i])
            else:
                row.append(None)
        matrix.append(row)

    return matrix


def print_display_list(sub_list, splash):
    page_width = 78
    clear_screen()
    header = f"  ID  WD  Date     Day  Status   Owner   Task\n {'-' * page_width}"
    print(splash)
    print(header)
    for i in sub_list:
        print(f"{i.id:>4}{i.work_day:>4}  {datetime.strftime(i.date, '%m/%d/%y %a')}"
            f"  {i.status.value:<8} {i.owner:<7} {i.task}")


def get_list_segments(todo_list: list, criteria: list):
    items_per_page = 15
    chunks = []
    sub_list = []
    short_list = list(filter(lambda x: x.status in criteria, todo_list))
    if not short_list:
        return []
    if len(short_list) <= items_per_page:
        chunks.append(short_list)
        return chunks
    for i, item in enumerate(short_list):
        if i != 0 and i % (items_per_page) == 0:
            chunks.append(sub_list)
            sub_list = []
            sub_list.append(item)
        else:
            sub_list.append(item)
    if sub_list:
        chunks.append(sub_list)
    return chunks


def get_accounting_period() -> datetime:
    while True:
        try:
            user_entry = input("Enter New Accounting Period (mm/yy): ").lower()
            date_parts = user_entry.split("/")
            if len(date_parts[-1]) == 4:
                date_parts[-1] = date_parts[-1][2:]
            if len(date_parts) == 3:
                # see if the "day" entered is valid
                _ = datetime.strptime(
                    date_parts[0] + "/" + date_parts[1] + "/" + date_parts[2][-2:], "%m/%d/%y"
                ) 
            user_date_str = date_parts[0] + "/01/" + date_parts[-1] 
            input_date = datetime.strptime(user_date_str, "%m/%d/%y")
            acct_period = cal.eom(input_date)
            user_confirm = input(
                f"\nNew accounting period is {acct_period.strftime('%x')}\n"
                f"Is this correct? (y/n): "
            ).lower()
            if user_confirm in ("y", "yes"):
                return acct_period

        except ValueError:
            print("Invalid entry. Please try again")


def get_date_from_user(prompt: str) -> datetime:
    while True:
        try:
            user_entry = input(f"{prompt} (mm/dd/yyyy): ").lower()
            date_parts = user_entry.split("/")
            if len(date_parts[-1]) == 2:
                date_parts[-1] = "20" + date_parts[-1]
            user_date_str = "/".join(date_parts)
            return datetime.strptime(user_date_str, "%m/%d/%Y")
        except ValueError:
            print("Invalid entry. Please try again")


def grab_new_date(wd_table: dict) -> tuple | None:
    """
    Gets a new date and the corresponding working day from the user and returns a
    tuple (date, working_day). If user elects 'Quit', then returns None
    """
    prompt = f"Enter the new date (mm/yy/dddd), working day (d), or (Q)uit: "
    while True:
        try:
            # Get input from user
            user_entry = input(prompt).lower()
            if user_entry in ("q", "quit"):
                return None
            if "/" in user_entry:
                date_parts = user_entry.split("/")
                if len(date_parts[-1]) == 2:
                    date_parts[-1] = "20" + date_parts[-1]
                user_date_str = "/".join(date_parts)
                date =  datetime.strptime(user_date_str, "%m/%d/%Y")
            else:
                date = cal.get_date_from_working_day(int(user_entry),wd_table)
                if not date:
                    raise KeyError

            # Test for Weekends and Holidays and if so, suggest earliest working day
            if not wd_table[date][1]:
                d = -1
                while not wd_table[date + timedelta(d)][1]:
                    d -= 1
                nearest_date = (date + timedelta(d), wd_table[date + timedelta(d)][1])
                date_category = wd_table[date][0]

                print(f"\n{date.strftime('%d-%b-%Y')} falls on a {date_category}."
                    f"\nNearest working day: {nearest_date[0].strftime('%m/%d/%y')}"
                    f"\nWeekday:{nearest_date[0].strftime('%a'):>16}"
                    f"\nWorking day:{' ' * 9}{nearest_date[1]:0>2}" 
                      )
                confirm = input("\nAccept this date? (Y/n): ").lower() or 'y'
                if confirm == 'y' or confirm == "yes":
                    return nearest_date
            else:
                print(f"\nNew Date: {date.strftime('%m/%d/%y'):>11}\nWeekday:{date.strftime('%a'):>8}"
                      f"\nWorking Day: {wd_table[date][1]:0>2}")
                confirm = input("\nAccept this date? (Y/n): ").lower() or 'y'
                if confirm == 'y' or confirm == "yes":
                    return date, wd_table[date][1]

        except KeyError:
            print("Date entered is out of range.")

        except ValueError:
            print("Invalid entry. Please try again")


def working_days_table() -> dict:
    """
    Returns a dictionary of working days for 90 days after the current period end. The dict keys 
    are a 90-day series of dates, with a tuple value (status: str, working_day: int). Status will
    be one of "weekend", "holiday", or "wd". 
    """
    holidays = pull_holidays() # Memoize this
    acct_period = read_accounting_period() # Memoize this
    wd = 0
    working_days = {}
    start_date = cal.first_of_next_month(acct_period)
    for offset in range(0, 91):
        this_date = start_date + timedelta(offset)
        if this_date in holidays:
            working_days[this_date] = ("holiday", None)
        elif this_date.weekday() > 4: 
            working_days[this_date] = ("weekend", None)
        else:
            wd += 1
            working_days[this_date] = ("wd", wd)
    return working_days

