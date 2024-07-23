import util


class Action:
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        self.function(*self.args, **self.kwargs)


class MenuItem:
    def __init__(self, name, action=None, submenu=None):
        self.name = name
        self.action = action
        self.submenu = submenu


class Menu:
    def __init__(self, title):
        self.title = title
        self.items = []

    def add_item(self, name, action=None, submenu=None):
        item = MenuItem(name, action, submenu)
        self.items.append(item)

    def centered_title(self, n, char):
        title_length = len(self.title)
        if title_length % 2 == 0:
            filler = (n - 1 - title_length) // 2
            return f"  {char * filler} {self.title} {char * (filler + 1)}"
        else:
            filler = (n - title_length) // 2
            return f"  {char * filler} {self.title} {char * filler}"

    def display(self):
        width = 35
        char = "-"
        splash_display = f"\n ======= MONTHLY CLOSE CALENDAR ======== \n\n"
        title_display = self.centered_title(width, char)
        util.clear_screen()
        print(f"{splash_display}{title_display}")
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. {item.name}")
        # print(f"\n'0' to Exit")


    def get_selection(self):
        while True:
            try:
                selection = int(input("\nSelection ('0' to Exit): "))
                if 0 <= selection <= len(self.items):
                    return selection
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def run(self):
        while True:
            self.display()
            selection = self.get_selection()
            if selection == 0:
                break
            else:
                selected_item = self.items[selection - 1]
                if selected_item.action:
                    selected_item.action.execute()
                elif selected_item.submenu:
                    selected_item.submenu.run()



