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


def pull_holidays(file_location: str) -> dict:
    """
    Reads text data from 'file_location' and returns a dict with key (datetime) representing the
    holiday date and value (str) representing the holiday description.
    """
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


def print_display_list(sub_list):
    page_width = 78
    clear_screen()
    splash = f"\n{' ' * 12}=============== UPDATE COMPLETION STATUS =============== \n\n"
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



