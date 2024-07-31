from datetime import datetime, timedelta
from main_func import *
import cal

test_date = datetime(2024, 6, 30)
test_date = test_date + timedelta(1)
test_result = cal.calc_first_monday(test_date)
test_result_string = test_result.strftime("%a %m/%d/%Y")
test_date_string = test_date.strftime("%a %m/%d/%Y")
week_start = cal.calc_calendar_weeks(cal.calc_first_monday(test_date))


def test_full_year():  
    print("--- Begin test data for test_full_year ---")
    for i in range(12):
        this_date = cal.calc_first_monday(datetime(2024, i + 1, 25))
        print(f"{i + 1:>5} {this_date.strftime('%a %m/%d/%Y')}")
    print("--- End test data ---\n")


def test_calendar_weeks():
    print("--- Begin test data for test_calendar_weeks ---")
    print(f"The first Monday for the date {test_date_string} is {test_result_string}")
    print()
    for k in week_start:
        dte_str = week_start[k].strftime("%a %m/%d/%Y")
        print(f"Calendar {k} begins with: {dte_str}" )
    print()
    print("--- End test data ---\n")


def test_weekly_display():
    print("--- Begin test data for test_weekly_display ---")
    print()
    for k in week_start:
        util.draw_week(week_start[k]) 
        print(" Item number 1")
        print()
    print("CELL_WIDTH ", util.CELL_WIDTH)
    print("--- End test data ---\n")


def test_holiday_import():
    period_end = datetime(2024, 10, 31)
    beg_date = period_end + timedelta(1)
    end_date = cal.eom(beg_date)
    path = "data/holidays.txt"
    hol = util.pull_holidays(path)
    print("--- Begin test data for test_weekly_display ---")
    print("Complete Holiday List:")
    for k in hol:
        dte_str = datetime.strftime(k, "%x")
        print(dte_str, hol[k])
    print("\nHolidays This Month:")
    print(f"Month End: {datetime.strftime(period_end, '%x')}")
    for k in hol:
        if k >= beg_date and k <= end_date:
            print(datetime.strftime(k, "%x"), hol[k])
    print("--- End test data ---\n")

def test_class_structure():
    todo_item = TODO(1, Status.OPEN, "Ethan", "ARO Accretion")
    print(todo_item)
    todo_item.date = datetime(2024, 7, 1)
    print(todo_item)
    todo_item.status = Status.STARTED
    print(todo_item)

def test_pull_todo_items():
    path = "data/close.txt"
    todo_list = pull_recurring_items(path)
    print(f"Wd Status   Owner   Task")
    print("---------------------------------------------------------")
    for item in todo_list:
        if item.status == Status.STARTED: 
            print(f"{item.work_day:>2}", end=" ")
            print(f"{item.status.value:<8}", end=" ")
            print(f"{item.owner:<7}", end=" ")
            print(item.task)

def test_assign_date():
    path = "data/close.txt"
    todo_list = pull_recurring_items(path)
    close_month = datetime(2024, 6, 30)
    todo_list = assign_date(todo_list, close_month)
    print(f"Wd Date     Status   Owner   Task")
    print("-----------------------------------------------------------------")
    for todo in todo_list:
        if todo.status == Status.OPEN:
            continue
        print (f"{todo.work_day:>2} {datetime.strftime(todo.date, '%x')} "
            f"{todo.status.value:<8} {todo.owner:<7} {todo.task}")


def test_weekly_view(date):
    print(date)


def test_read_write_funcs(working_list):
        # --- Testing updated read_data() and write_data() to incorporate self.id class attribute
    for todo in working_list:
        if todo.id == 38:
            todo.update_status('s')
        if todo.id == 60:
            todo.owner = "Jeff"
        #     todo.task = "Arm wrestle Hercules"
        #     todo.update_status('c')
        # if todo.id == 59:
        #     todo.update_status('c')
        #     todo.owner = "Sisyphus"
        #     todo.task = "Roll the bolder back up the hill (again)"

        for todo in working_list:
            print(f"{todo.id:>2} {todo.status.value:<10} {todo.owner:<8} {todo.task}")

        write_data(working_list)


def test_get_date():
# ----- test get_date function -----
    test_date = util.get_accounting_period()
    print(f"\ntest_date= {test_date.strftime('%x')}")


def test_init_month_end():
# ----- test init_month_end func -----
    todo_list, test_date = init_month_end()
    if test_date and todo_list:
        display_weekly_calendar(todo_list, test_date)


def test_data_persist_write_status_update():
# ----- test that data persists after change in status -----
    accounting_period = util.get_accounting_period()
    working_list = read_data()
    update_status(working_list, [Status.OPEN, Status.STARTED], Status.COMPLETE)
    write_data(working_list)
    display_weekly_calendar(working_list, accounting_period)

def test_data_persist_after_write():
    accounting_period = datetime(2024, 7, 31)
    working_list = read_data()
    display_weekly_calendar(working_list, accounting_period)


def test_read_write_accounting_period():
    input_accounting_period = util.get_accounting_period()
    write_accounting_period(input_accounting_period)
    output_accounting_period = read_accounting_period()
    print(f"Input Date: {input_accounting_period.strftime('%x')}")
    print(f"Output Date: {output_accounting_period.strftime('%x')}")

def main():
    # test_init_month_end()
    test_read_write_accounting_period()

if __name__ == "__main__":
    main()
