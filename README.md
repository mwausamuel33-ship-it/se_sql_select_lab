## Introduction

Welcome to the SQL Lab! In this assessment, you will learn how to use **SQL (Structured Query Language)** to work with databases in Python. 

**The Scenario:** You're working as a data specialist in the HR department of the fictional Northwind Company. Your job is to extract and analyze employee data from the company database. Instead of manually looking through spreadsheets, you'll use SQL to quickly get exactly the data you need!

**What You'll Learn:**
- How to connect to a database using Python
- How to write SQL queries to retrieve data
- How to filter, transform, and organize data using SQL functions
- How to use aliases and conditional logic (CASE statements) to make your results clearer

All your work will go in the `main.py` file, and the employee data is stored in the `data.sqlite` file. You can test your work anytime by running `pytest` or checking the print statements with `python3 main.py`.

## Learning Objectives

By the end of this lab, you'll be able to:

✓ **Connect to a database** - Set up a Python connection to a SQLite database file  
✓ **Write SELECT queries** - Choose specific columns from a table using `SELECT`  
✓ **Order and rename columns** - Arrange columns the way you want and use `AS` to rename them  
✓ **Use conditional logic** - Use `CASE` statements to categorize data  
✓ **Manipulate text** - Extract parts of text with `SUBSTR()` and get text length with `LENGTH()`  
✓ **Do math with data** - Calculate totals with `SUM()`, `ROUND()`, and multiplication  
✓ **Work with dates** - Extract day, month, and year from date strings

## Getting Started

### Prerequisites
Before you start, you need to set up your Python environment:

1. **Install dependencies:** Run `pipenv install` to download and install the required libraries (sqlite3 and pandas)
2. **Activate the environment:** Run `pipenv shell` to start using the environment

### How to Test Your Work
- **Run all tests:** `pytest` - This checks if all your solutions are correct
- **Run one test at a time:** `pytest -x` - Stops after the first test (useful for debugging)
- **See print output:** `python3 main.py` - Runs your code and shows any print statements

## Part 1: Connecting to Data

The database file (`data.sqlite`) contains real company data from Northwind, including products, customers, and employees. In this lab, you'll focus mainly on the **employees** table.

### How SQL Results Work with Python
We'll use `pd.read_sql()` to run SQL queries and get results as a **pandas DataFrame** (basically a table in Python):

```python
# This runs a SQL query and loads the results into a DataFrame
df_answer = pd.read_sql("""SELECT * FROM some_table""", connection)
```

Think of it like this:
- **SELECT \*** = "Get all columns"
- **FROM some_table** = "From this table"
- The result becomes a DataFrame with rows and columns, just like a spreadsheet!

### Step 1: Set Up Your Connection

**Task:** Import the libraries you need and connect to the database.

In `main.py`, you'll see:

```python
# STEP 1A
# Import SQL Library and Pandas

# STEP 1B
# Connect to the database
conn = None
```

**What you need to do:**
1. Import `sqlite3` - This lets you work with SQL databases
2. Import `pandas as pd` - This lets you work with data as tables
3. Create a connection to `data.sqlite` by using `sqlite3.connect('data.sqlite')`

**Try it out:** After you set up the connection, run this code to see all employees:

```python
# Add code below and run file to see data from employees table
employee_data = pd.read_sql("""SELECT * FROM employees""", conn)
print("---------------------Employee Data---------------------")
print(employee_data)
print("-------------------End Employee Data-------------------")
```

This will print out a table with all the employees and their information.

## Part 2: Selecting Specific Columns

In this part, you'll learn to choose exactly which columns you want from your data. Instead of getting all columns (with `SELECT *`), you'll pick specific ones.

### Step 2: Select Specific Columns

**Task:** Get the employee number and last name for all employees. Only include these two columns.

```python
# STEP 2
# Replace None with your code
df_first_five = None
```

**Hint:** Use `SELECT` to list which columns you want, separated by commas. For example:
```sql
SELECT columnName1, columnName2 FROM tableName
```

### Step 3: Reverse Column Order

**Task:** Do the same as Step 2, but put the last name first and employee number second.

```python
# STEP 3
# Replace None with your code
df_five_reverse = None
```

**Why this matters:** Sometimes the order of columns matters for how you want to see your data. SQL lets you arrange columns any way you like!

## Part 3: Renaming Columns with Aliases

### Step 4: Use Aliases to Rename Columns

**Task:** Repeat Step 3, but rename the `employeeNumber` column to just `ID`.

```python
# STEP 4
# Replace None with your code
df_alias = None
```

**What's an alias?** An alias is a temporary nickname for a column. Use the `AS` keyword:

```sql
SELECT columnName AS newName FROM tableName
```

**Example:**
```sql
SELECT firstName AS 'First Name', lastName AS 'Last Name' FROM employees
```

This makes your column headers clearer and easier to read!

## Part 4: Using CASE Statements

### Step 5: Categorize Employees with CASE

**Task:** Create a new column called `role` that categorizes employees as either "Executive" or "Not Executive".
- **Executive:** President, VP Sales, VP Marketing
- **Not Executive:** Everyone else

```python
# STEP 5
# Replace None with your code
df_executive = None
```

**What's a CASE statement?** It's like an `if-else` statement in SQL. Here's the pattern:

```sql
CASE 
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE defaultResult
END AS columnName
```

**Example hint:** If we wanted to categorize by Managers:

```sql
WHEN jobTitle = "Sales Manager (APAC)" OR jobTitle = "Sale Manager (EMEA)" OR jobTitle = "Sales Manager (NA)" THEN "Manager"
```

You'll do something similar, but for the three executive roles!

## Part 5: String Functions (Text Manipulation)

SQL has built-in functions to work with text. Here are two useful ones:

- **`LENGTH(text)`** - Counts how many characters are in a piece of text
- **`SUBSTR(text, start, length)`** - Pulls out a piece of text starting at a position

### Step 6: Find Text Length

**Task:** Get the length (number of characters) of each employee's last name. Return only this data in a column called `name_length`.

```python
# STEP 6
# Replace None with your code
df_name_length = None
```

**Hint:** Use the `LENGTH()` function on the `lastName` column.

### Step 7: Extract Part of Text

**Task:** Get the first two letters of each employee's job title. Create a column called `short_title`.

```python
# STEP 7
# Replace None with your code
df_short_title = None
```

**Hint:** Use `SUBSTR(column, 1, 2)` to get the first 2 characters:
- First `1` = start at position 1
- Second `2` = take 2 characters

## Part 6: Math and Date Functions

Now you'll work with the `orders` and `orderDetails` tables to practice math and date manipulation.

### First, Look at Order Details

Run this code to see what the order data looks like:

```python
# Add the code below and run the file to see order details data
order_details = pd.read_sql("""SELECT * FROM orderDetails;""", conn)
print("------------------Order Details Data------------------")
print(order_details)
print("----------------End Order Details Data----------------")
```

You'll see columns like `priceEach` and `quantityOrdered` - perfect for doing math!

### Step 8: Calculate Total Revenue

**Task:** Find the total amount for ALL orders combined.

To do this:
1. Multiply `priceEach` × `quantityOrdered` for each item
2. Round each result to the nearest whole number (using `ROUND()`)
3. Add them all up using `SUM()`

```python
# STEP 8
# Replace None with your code
sum_total_price = None
```

**Hint:** You can write the calculation right in your SELECT statement:

```python
sum_total = pd.read_sql("""
SELECT SUM(ROUND(priceEach * quantityOrdered)) as total
FROM orderDetails
""", conn).iloc[0].values
```

The `.iloc[0].values` at the end gets the first (and only) row's value.

### Step 9: Parse Dates

**Task:** Break down each order date into separate day, month, and year columns.

The dates are stored as `YYYY-MM-DD` (like `2003-01-06`). You need to extract:
- **Day** (the `06`)
- **Month** (the `01`)
- **Year** (the `2003`)

And display them in Day/Month/Year format.

```python
# STEP 9
# Replace None with your code
df_day_month_year = None
```

**Hint:** Use `SUBSTR()` to pull out pieces of the date string:
- Position 1-4 = Year
- Position 6-7 = Month
- Position 9-10 = Day

### Finish Up

Don't forget to close your database connection when you're done:

```python
conn.close()
```

**Why?** Closing connections is good practice - it frees up resources and keeps your database safe.