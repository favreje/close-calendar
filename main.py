from datetime import datetime, timedelta
import time
from main_func import *
import front_end as fe
import test
import util

def main():
    # todo_list = pull_recurring_items(todo_file_location) # refactor: change name to pull_recurring_items()
    # todo_list = assign_date(todo_list, accounting_period)
    # simple_report(todo_list, ["open", "started"])
    # write_data(todo_list, accounting_period)
    # display_weekly_calendar(working_list, accounting_period)
    # simple_report(working_list, ["all"])

    accounting_period = datetime(2024, 6, 30)
    working_list = read_data(accounting_period)

    # ----- Implementation of the Menu System -----
    main_menu = fe.Menu("Main Menu")
    report_menu = fe.Menu("Reports")
    status_update_menu = fe.Menu("Change Task Status")
    modify_task_menu = fe.Menu("Modify Tasks")

    main_menu.add_item("Reports", submenu=report_menu)
    main_menu.add_item("Change Task Status", submenu=status_update_menu)
    main_menu.add_item("Modify Tasks", submenu=modify_task_menu)
    report_menu.add_item("Weekly View", action=fe.Action(display_weekly_calendar,
                            working_list, accounting_period))
    report_menu.add_item("List View - Open and Started Items", action=fe.Action(simple_report,
                            working_list, ["open", "started",]))
    report_menu.add_item("List View - Completed Items", action=fe.Action(simple_report,
                            working_list, ["complete",]))
    report_menu.add_item("List View - All Items", action=fe.Action(simple_report,
                            working_list, ["all",]))
    status_update_menu.add_item("Update Status to Complete", action=fe.Action(update_status,
                                                              working_list, Status.OPEN))

    main_menu.run()

    # display_weekly_calendar(working_list, accounting_period)
    # update_status(working_list, Status.OPEN)
    # display_weekly_calendar(working_list, accounting_period)

if __name__ == "__main__":
    main()

