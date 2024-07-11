from datetime import datetime, timedelta


SPACING = " " * 15
UNDERLINE = "-" * 214

# length of date + spacing on each end - indentation on each end
CELL_WIDTH = 6 + (len(SPACING) * 2) 


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
