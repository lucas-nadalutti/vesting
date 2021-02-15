Vesting Schedule Generation


How to Run

- Execute the following on command line:
    python3 /path/to/vesting.py [csv file name] [target date] [digits of precision]

    -- Note: any new example CSV files must be placed in "files" directory

- To run tests, execute the following:
    python3 -m unittest discover


About Key Design Decisions

- This solution was implemented using Domain Driven Design approach in order to keep the code clean and extensible

- Python was the language of choice for readability as well as making the solution easier to both implement and run (i.e.
no need to build and no external dependencies needed)


Assumptions

- Inputs will always include vest events before cancel events for a given employee. The examples meet this premise, and
not assuming this would result in a considerably more complex code with little upside in terms of code evaluation