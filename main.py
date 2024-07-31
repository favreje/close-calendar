from main_func import *
import front_end as fe

def main():

    # ----- Gather data for the current accounting cycle at application launch -----
    accounting_period = read_accounting_period
    working_list = read_data()

    # ----- Configuration of the Menu System -----
    main_menu = fe.Menu("Main Menu", is_main_menu=True)
    report_menu = fe.Menu("Reports")
    status_update_menu = fe.Menu("Change Task Status")
    modify_task_menu = fe.Menu("Modify Tasks")
    initiate_month_end_menu = fe.Menu("Initiate New Month End Data File")

    main_menu.add_item("Reports", submenu=report_menu)
    main_menu.add_item("Change Task Status", submenu=status_update_menu)
    main_menu.add_item("Modify Tasks", submenu=modify_task_menu)
    main_menu.add_item("Initiate New Month End Data File")
    report_menu.add_item("Weekly View", action=fe.Action(display_weekly_calendar,
                            working_list, accounting_period))
    report_menu.add_item("List View - Open and Started Items", action=fe.Action(simple_report,
                            working_list, ["open", "started",]))
    report_menu.add_item("List View - Completed Items", action=fe.Action(simple_report,
                            working_list, ["complete",]))
    report_menu.add_item("List View - All Items", action=fe.Action(simple_report,
                            working_list, ["all",]))
    status_update_menu.add_item("Update Status to Complete", action=fe.Action(update_status,
                                  working_list, [Status.OPEN, Status.STARTED], Status.COMPLETE))

    main_menu.run()

main()
