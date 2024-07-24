from datetime import datetime, timedelta
import time
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

    # write_data(todo_list, accounting_period)
    working_list = read_data(accounting_period)
    # display_weekly_calendar(working_list, accounting_period)
    # simple_report(working_list, ["all"])

    # # ----- Implementation of the Menu System -----
    # main_menu = fe.Menu("Main Menu")
    # report_menu = fe.Menu("Reports")
    # status_update_menu = fe.Menu("Change Task Status")
    # modify_task_menu = fe.Menu("Modify Tasks")
    #
    # main_menu.add_item("Reports", submenu=report_menu)
    # main_menu.add_item("Change Task Status", submenu=status_update_menu)
    # main_menu.add_item("Modify Tasks", submenu=modify_task_menu)
    # report_menu.add_item("Weekly View", action=fe.Action(display_weekly_calendar,
    #                         working_list, accounting_period))
    # report_menu.add_item("List View - Open and Started Items", action=fe.Action(simple_report,
    #                         working_list, ["open", "started",]))
    # report_menu.add_item("List View - Completed Items", action=fe.Action(simple_report,
    #                         working_list, ["complete",]))
    # report_menu.add_item("List View - All Items", action=fe.Action(simple_report,
    #                         working_list, ["all",]))
    #
    # main_menu.run()

    def print_display_list(sub_list):
        page_width = 78
        util.clear_screen()
        splash = f"\n{' ' * 12}=============== UPDATE COMPLETION STATUS =============== \n\n"
        header = f"  ID  WD  Date     Day  Status   Owner   Task\n {'-' * page_width}"
        print(splash)
        print(header)
        for i in sub_list:
            print(f"{i.id:>4}{i.work_day:>4}  {datetime.strftime(i.date, '%m/%d/%y %a')}"
                f"  {i.status.value:<8} {i.owner:<7} {i.task}")


    display_weekly_calendar(working_list, accounting_period)
    display_list = get_selected_item(working_list, Status.OPEN)
    if display_list:
        display_list_len = len(display_list)
        sub_list_num = 0
        while True:
            util.clear_screen()
            print_display_list(display_list[sub_list_num])
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
                    for i, todo in enumerate(working_list):
                        if todo.id == sel_num:
                            print(f"  ID  WD  Date     Day  Status   Owner   Task\n {'-' * 78}\n"
                                    f"{todo.id:>4}{todo.work_day:>4}  "
                                    f"{datetime.strftime(todo.date, '%m/%d/%y %a')}"
                                    f"  {todo.status.value:<8} {todo.owner:<7} {todo.task}")
                            confirm = input("\nUpdate this item? (Y/n) ").lower() or 'y'
                            if confirm == 'y' or confirm == "yes":
                                working_list[i].update_status('c')
                                display_list = get_selected_item(working_list, Status.OPEN)
                            break
                else:
                    input(f"\nSelection is out of range. Please select again... ")



    display_weekly_calendar(working_list, accounting_period)

if __name__ == "__main__":
    main()

