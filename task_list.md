# Open Items

## Main Concepts
1. Build out display_weekly_calendar
1. Write a function that writes the todo list back to a file
    - think about how I want to store data, since it's a really small data set 
    - a simple text file will probably do
    - But... it may be a good idea to practice working with a database
1. Build out modules to interact with data
    - update status
    - change owner
    - change  working day
    - modify task description
    - add and delete todo items
1. Determine how to most efficiently interact with the todo list before building out the front end
    - pass command line flags
    - build a simple command line text menu
    - build a tui interaction mode

## Bugs and  Refactoring
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

