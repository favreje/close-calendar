# TO-DO List

## Immediate
1. Change parameter for the status to a list in order to include more than one (like the code for
   'simple_report')
1. update_status() - add a third parameter
   - Parameters: (todo_list: list, current_status: list,new_status: Status)
   - Broadens the functionality to accept any combination of Status objects and modify to any type

## Current Focus
### Update Status Function
1. Complete the module to include a final hook that writes to disk after status updates are
   completed.
    - I think reasonable to do this when user enters 'Done' for a batch of updates
    - As opposed to after every TODO object update
1. Add the module to the front-end menu system
1. Add variations of this to the menu system
    1. To change from 'open' / 'started' to 'complete' (modify the existing one to include 'started')
    1. To change from 'open' to 'started'
    1. To revert a 'complete' item to 'open' 
    1. Consider a user-defined status update
        - Accept user input for the desired current status(es) and the new status to operate upon,
          and then run the module
1. More robust error handling of user input (Don't go crazy - we ultimately want a web-based front
   end)

### General
1. Menu should display the current 'Accounting Period' in the splash header
1. Add 'Change Date' module next - then it would be usable while I continue to update functionality
1. Rethink accounting month check. When we have a working file, no need to continue to check for
   accounting month. The user can select 'initiate a new accounting month' from the menu.
    - When initiating a new month, include warnings about "will overwrite existing date; cannot be
    undone, etc."
    - or better: create a backup before initiating a new month, in case user wants to revert

## Main Concepts
1. Web-based front-end would include a check-box type object, except with three states:
   - A circle type bullet object
   - Bullet object would toggle between
        - red=open
        - yellow=started
        - green=complete
   - Save this state to the server
1. Eventually I'd like to add a separate module for general 'todo' items that are separate from the
   monthly recurring task list.
   - Think about what fields get inherited from TODO class, and what fields are unique to this new
     class (e.g. 'tags' for item categories may be useful in a general 'todo' list, whereas
   'working day' would not be)
   - probably want to write this to disk in a separate file
1. Build a graceful exit from wrong accounting month scenario
    - Make initial population from 'recurring items list' a once a month activity
    - After which, the default would be to load the working file at start up, unless the user asks
    to initialize a new working file.
    - Warn user if the accounting month in the saved file differs from the working accounting month:
    ```bash
    "A working file for 6/30/24 already exists. Are you sure you want to overwrite it?"
    ```
1. ADDING records - when assigning self.id, increment the last id in the list: todo_list[-1].id + 1
1. Build out modules to interact with data
    - initialize a new accounting month - pull the recurring items into a new working month data
    file. Include appropriate warnings to user that they risk overwriting an existing file
    - Methods in the TODO class:
        - update status
        - change owner
        - change  working day
        - modify task description
    - add and delete todo items
        - add would include a date, but not a working day.
        - a function would be needed to determine the working day, raise exceptions for bad date
        formats, out of bound dates, weekends (push to previous Friday)
1. Build a web app front end (keep it simple at first)


## Bugs and  Refactoring
1. General refactoring to move util or cal functions out of the main_func.py module.
    - Consider a separate module for report display
1. assign_date func - Consider making the holiday_table a parameter to the function instead of a
   call from within the function *if* the table will be used more than once
1. Make sure working days per the source text file are constrained to those
   within the working_day_table range.
    - a working day of 35 in the text file throws a KeyError
    - Consider whether we want to constrain the working days to only the subsequent month for the
    close period (and throw an exception here), or lengthen the close period - maybe 90 days? - and
    only throw an exception if outside of that range.
    - But in either case something more elegant than a date of 01/01/01 for out-of-bound objects,
    as currently written

## Error Handling
1. Reading text input file
    - handle exception: working day must be numeric
    - handle exception: date must be numeric and must be formatted as 'mm/dd/yy'
1. Print report
    - handle exception: status string cannot be longer than 2 items

