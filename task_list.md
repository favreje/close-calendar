# Open Items

## Main Concepts
1. Build out display_weekly_calendar
1. Build out modules to interact with data
    - update status
    - change owner
    - change  working day
    - modify task description
    - add and delete todo items
1. Determine how to most efficiently interact with the todo list before I get a chance to build a
front end
    - pass command line flags
    - build a simple command line text menu
    - build a tui interaction mode

## Bugs and  Refactoring
1. assign_date func - Consider making the holiday_table a parameter to the function instead of a
call from within the function if the table will be used more than once
1. Make sure working day per the source text file constrained to only those within the
working_day_table range. (e.g. a working day of 35 in the text file will throw a KeyError)
1. Need something more elegant. Consider whether we want to constrain the working days to only the
subsequent month for the close period (and throw an exception here), or lengthen the close
period - maybe 90 days? - and only throw an exception if outside of that range. But in either case
not a date of 01/01/01. 

