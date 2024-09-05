# TO-DO List

## Immediate
1. For write_report function, add exception handling for PermissionError if the file is opened in
   another application (e.g., Excel)
1. Function to add a task to the database

## Current Focus
1. Add functionality to simple_report() by adding a 'filtered_by' parameter
    - Currently hard coded to filter by status only
    - Filter by multiple TODO variables (e.g., owner and status; owner and date, etc.)
    - Probably will require a decorator function wrapper
1. Add more robust error handling of user input to update_status()
    - Don't go crazy - we ultimately want a web-based front end
1. Create a backup before initiating a new month, in case user wants to revert
1. Add exception testing to the initial read_data() call from main()
    - ensure file exists
    - ensure file is in correct format (i.e., returns at least one TODO record)
        - Not exactly sure how to do this; maybe just a try / except block that will point the user
          to initiate a new month or recover from backup if there is bad data?
1. Add an Owner table that would include relevant employee information (Name, title, contact_info,
   sort_order for reports)

## Issues
1. Initiate_month_end_menu difficult to get the current Menu class to return a value
    - Consider a State class the encapsulates any return parameters
    - Use this class to pass data around from one menu module to the next.
    - Similar to an api approach. 

## Main Concepts
1. Refactor to make the app more OOP focused (currently uses classes only to store data objects)
1. Web-based front-end would include a check-box type object, except with three states:
    - A circle type bullet object
    - Bullet object would toggle between
        - red=open
        - yellow=started
        - green=complete
    - Save this state to the server
1. Feature: I'd like to add a separate module for general 'todo' items that are separate from the
   monthly recurring task list.
    - Think about what fields get inherited from TODO class, and what fields are unique to this new
     class (e.g. 'tags' for item categories may be useful in a general 'todo' list, whereas
   'working day' would not be)
    - probably want to write this to disk in a separate file
1. Feature: Write a stylized list report to Excel. Various options to include:
    - all info sorted by working date for initial file for the full team
    - filter by Owner, sorted by working date for individual members
    - filter by Owner, with 'open' items only for individual team member updates

1. ADDING records - when assigning self.id, increment the last id in the list: todo_list[-1].id + 1
1. Feature: When initiating a new accounting month, ask user if they would like to use the existing
   file as the template or the previous recurring file. If the existing, update the recurring file
   to match the existing file
    - maybe a more elegant feature: show the user the differences and ask to select lines to add to
      the recurring file on a go-forward basis.
1. Build out modules to interact with data
    - Methods in the TODO class:
        - change working day and date
        - modify task description
    - add and delete todo items
        - add would include a date, but not a working day.
        - a function would be needed to determine the working day, raise exceptions for bad date
        formats, out of bound dates, weekends (push to previous Friday)
1. Build a web app front end (keep it simple at first)


## Bugs and  Refactoring
1. Need to refactor update_status() and change_due_date() to make it DRY (it does not reuse any of
   the task selection code!) 
1. update_status() has an "object of type none is not subscriptable" issue
    - the code runs - I don't think it would ever return None, but maybe a mutability issue, so add
      checks
    - for similar reasons, also check for subscript value being out of range 
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

