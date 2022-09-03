import re
import sqlite3
from datetime import date, datetime

def create_database():
    """Creates a new empty database"""
    con = sqlite3.connect("expenses.db")
    c = con.cursor()
    c.execute("""DROP TABLE IF EXISTS expenses""")
    c.execute("""CREATE TABLE expenses (
        remaining FLOAT,
        budget FLOAT,
        description TEXT,
        expense FLOAT,
        day INT,
        month INT,
        year INT
    )""")
    c.execute("""INSERT INTO expenses VALUES (0, 0, '', 0, 0, 0, 0)""")
    con.commit()
    con.close()


def showAll():
    """Shows all the entries in the database"""
    con = sqlite3.connect("expenses.db")
    c = con.cursor()
    c.execute("SELECT * FROM expenses")
    entries = c.fetchall()
    for entry in entries:
        print(entry)
    con.close()


def enter_expense(amount, description="No description"):
    """Enters an expense into the database"""
    con = sqlite3.connect("expenses.db")
    c = con.cursor()
    current_date = date.today()
    day = current_date.day
    month = current_date.month
    year = current_date.year
    c.execute("SELECT rowid, remaining, budget FROM expenses ORDER BY rowid DESC LIMIT 1")
    result = c.fetchone()
    remaining = result[1] - amount
    budget = result[2] 
    c.execute("INSERT INTO expenses VALUES (?,?,?,?,?,?,?)", (remaining, budget, description, amount, 
    day, month, year)) 
    con.commit()
    con.close()  


def enter_new_budget(new_budget):
    """Enters a new budget into the database. The remainder is innitialy set to the 
    value of the budget"""
    con = sqlite3.connect("expenses.db")
    c = con.cursor()
    current_date = date.today()
    day = current_date.day
    month = current_date.month
    year = current_date.year
    c.execute("INSERT INTO expenses VALUES (?,?,?,?,?,?,?)", (new_budget, new_budget, "", 0, day, month, year))
    result = c.fetchone()
    con.commit()
    con.close()


def get_balance():
    """Returns the current balance/remainder of funds"""
    con = sqlite3.connect("expenses.db")
    c = con.cursor()
    c.execute("SELECT rowid, remaining FROM expenses ORDER BY rowid DESC LIMIT 1")
    result = c.fetchone()
    remaining = result[1]
    con.close()
    return remaining


def get_budget():
    """Returns the current budget"""
    con = sqlite3.connect("expenses.db")
    c = con.cursor()
    c.execute("SELECT rowid, budget FROM expenses ORDER BY rowid DESC LIMIT 1")
    result = c.fetchone()
    budget = result[1]
    con.close()
    return budget


def get_entries_on_date(date):
    """Returns all expenses on the provided date in a list of tupples.  
    It takes in dd/mm/yyyy, dd-mm-yyyy, yyyy/mm/dd, yyyy-mm-dd"""

    #making sure the user provided a valid date, if not the function returns none
    match1 = re.match("[0-9]{2}/[0-9]{2}/[0-9]{4}", date)
    match2 = re.match("[0-9]{2}-[0-9]{2}-[0-9]{4}", date)
    match3 = re.match("[0-9]{2}.[0-9]{2}.[0-9]{4}", date)

    match4 = re.match("[0-9]{4}/[0-9]{2}/[0-9]{2}", date)
    match5 = re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date)
    match6 = re.match("[0-9]{4}.[0-9]{2}.[0-9]{2}", date)

    if match1 or match2 or match3:
        day = int(date[0:2])
        month = int(date[3:5])
        year = int(date[6:])
    elif match4 or match5 or match6:
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:])
    else:
        return 

    con = sqlite3.connect("expenses.db")
    c = con.cursor()
    c.execute("""SELECT expense, description, day, month, year FROM expenses WHERE day = (?) and month = (?) and year = (?)
    and expense > 0""",
    (day, month, year))
    result = c.fetchall()
    con.close()
    return result


def get_entries_on_month(month_year):
    """Returns all the expenses in a given month of a specified year.
    The result is returned as a list of tupples"""
    #making sure the user provided a valid date, if not the function returns none
    match1 = re.match("[0-9]{2}/[0-9]{4}", month_year)
    match2 = re.match("[0-9]{2}-[0-9]{4}", month_year)
    match3 = re.match("[0-9]{2}.[0-9]{4}", month_year)
    
    if match1 or match2 or match3:
        month = int(month_year[0:2])
        year = int(month_year[3:])
    else:
        return

    con = sqlite3.connect("expenses.db")
    c = con.cursor()
    c.execute("""SELECT  expense, description, day, month, year FROM expenses 
    WHERE month = (?) and year = (?) and expense > 0""", (month, year))
    result = c.fetchall()
    con.close()
    return result
