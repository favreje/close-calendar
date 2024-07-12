import os


splash_display = f"\n   ===== MONTHLY CLOSE CALENDAR ====="


def menu_update():
    update_menu_display = (
            f"\n\n"
            f"------------- Update Status -------------\n\n"
            f"1. (O)pen\n"
            f"2. (S)tarted\n"
            f"3. (C)complete\n"
            f"\n\n\n"
            f"9. (B)ack to Main Menu\n"
            f"-----------------------------------------\n\n"
    )
    user_input = " "
    while user_input[0] not in "9Qq":
        print(splash_display)
        print(update_menu_display)



def menu_loop():
    main_menu_display = (
            f"\n\n"
            f"--------------- Main Menu ---------------\n\n"
            f"1. (U)pdate status\n"
            f"2. (R)eports\n"
            f"3. (T)asks (add, delete, modify)\n"
            f"\n\n\n"
            f"9. (Q)uit\n"
            f"-----------------------------------------\n\n"
    )
    user_input = " "
    while user_input[0] not in "9Qq":
        os.system("clear")
        print(splash_display)
        print(main_menu_display)
        user_input = input("Selection: ")

        if user_input[0] in "1Uu":
            menu_update()


# menu_loop()
