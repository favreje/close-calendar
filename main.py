from main_func import *
import front_end as fe

def main():

    all = [Status.OPEN, Status.STARTED, Status.COMPLETE]

    # ----- Gather data for the current accounting cycle at application launch -----
    acct_period = util.read_accounting_period()
    working_list = read_data()

    # ----- Configuration of the Menu System -----
    main_menu = fe.Menu("Main Menu", acct_period, is_main_menu=True)
    report_menu = fe.Menu("Reports", acct_period)
    status_update_menu = fe.Menu("Change Task Status", acct_period)

    main_menu.add_item("Reports", submenu=report_menu)
    main_menu.add_item("Change Task Status", submenu=status_update_menu)
    main_menu.add_item("Change Due Date", action=fe.Action(change_due_date, working_list))
    main_menu.add_item("Initiate New Month End", action=fe.Action(init_month_end, acct_period)) 

    report_menu.add_item("Weekly View", action=fe.Action(display_weekly_calendar,
                            working_list, acct_period))

    report_menu.add_item("List View by Owner - Open and Started Items", action=fe.Action(report_by_owner,
                            working_list, [Status.OPEN, Status.STARTED,]))

    report_menu.add_item("List View by Owner - Started Items", action=fe.Action(report_by_owner,
                            working_list, [Status.STARTED,]))

    report_menu.add_item("List View by Owner - Completed Items", action=fe.Action(report_by_owner,
                            working_list, [Status.COMPLETE,]))

    report_menu.add_item("List View by Owner - All Items", action=fe.Action(report_by_owner,
                            working_list, all))

    report_menu.add_item("List View by Date - All Items",
                            action=fe.Action(report_by_day, working_list, all))

    status_update_menu.add_item("Update Status to Complete", action=fe.Action(update_status,
                                  working_list, [Status.OPEN, Status.STARTED], Status.COMPLETE))

    status_update_menu.add_item("Update Status to Started", action=fe.Action(update_status,
                                  working_list, [Status.OPEN,], Status.STARTED))

    status_update_menu.add_item("Revert Status to Open", action=fe.Action(update_status,
                                  working_list, [Status.COMPLETE, Status.STARTED], Status.OPEN))

    main_menu.run()

main()
