Introduction
In this assessment lab, you will explore basic techniques for retrieving and transforming data using SQL (Structured Query Language) in Python. You will be working with the employees table stored in the data.sqlite file and your code for this lab will be in main.py. You can run pytest and use print statements to check your code as you go. Imagine that you are working within the HR department of the fictional Northwinds Company as a data specialist/analyst and need to be able to easily access select employee records. SQL is just the tool you need!

SQL is a powerful language that allows us to interact with relational databases and perform various operations on the data. By leveraging SQL queries, we can efficiently retrieve specific subsets of data, create meaningful aliases for improved readability, transform selected columns using CASE statements, and utilize built-in SQL functions to perform advanced transformations.

Learning Objectives
Connect to a SQL Database file
Use SELECT in SQL to select columns from a database
Use SQL built-in functions to manipulate the values of the given database
Part 1: Connecting to Data
A SQL database file has been provided that contains the Northwind company's product, customer and employee data (fictional). For the scope of this assessment you will focus mostly on the employees tables. You will be asked to retrieve specific information/data using SQL queries in tandem with Pandas to load the results into a DataFrame.

Example:

df_answer = pd.read_sql("""SELECT * FROM some_table""", connection)
Start by running pipenv install and pipenv shell. You can run the test suite at any time to check your work with pytest or pytest -x if you want to just run 1 test at a time. You can run the file to check print statement outputs with python3 main.py.

Step 1
In main.py import the necessary libraries, sqlite3 and pandas. Use the standard alias for the pandas library. Create a connection to the data.sqlite database file and store it as the variable conn.

# STEP 1A
# Import SQL Library and Pandas

# STEP 1B
# Connect to the database
conn = None
As previously stated, this database contains multiple tables but for this assessment you will focus on querying data from the employees table and later from the orderDetails table. Below, we have provided code that selects all columns and rows from the employees table for you to use as reference.

# Add code below and run file to see data from employees table
employee_data = pd.read_sql("""SELECT * FROM employees""", conn)
print("---------------------Employee Data---------------------")
print(employee_data)
print("-------------------End Employee Data-------------------")
Part 2: Basic Select Filtering
Step 2
Assign the variable df_first_five to the employee number and last name from all employees in the employees table in the database. Your result should only contain those two columns.

# STEP 2
# Replace None with your code
df_first_five = None
Step 3
Repeat Step 2, but have the last name come before the employee number and assign to df_five_reverse.

# STEP 3
# Replace None with your code
df_five_reverse = None
Part 3: Aliasing in Select
Step 4
Repeat step 3, but this time use an alias to rename the employee number column as 'ID' and assign to df_alias.

# STEP 4
# Replace None with your code
df_alias = None
Step 5
Use CASE to bin where the jobTitles of President, VP Sales, or VP Marketing have the role of "Executive", and the rest of the employes are "Not Executive".




Define the result of the CASE as a new column called role. Assign to the variable df_executive.


Hint: For the WHEN clause if we were looking at Managers, we'd have:

WHEN jobTitle = "Sales Manager (APAC)" OR jobTitle = "Sale Manager (EMEA)" OR jobTitle = "Sales Manager (NA)" THEN "Manager"
# STEP 5
# Replace None with your code
df_executive = None
Part 5: Built-in Functions - Strings
Step 6
Find the length of the last name for all employees, return only this data as a new column called name_length. Assign to df_name_length.

# STEP 6
# Replace None with your code
df_name_length = None
Step 7
Return only one new column called short_title, that contains the first two letters of each persons job title. Assign to df_short_title.

# STEP 7
# Replace None with your code
df_short_title = None
Part 6: Built-in Functions - Numerics
Bring in another table from the database
In the code below we have provided a look at a new table within the database provided. This table contains data pertaining to orders placed with the company and has some good numerical and date columns to explore.

# Add the code below and run the file to see order details data

order_details = pd.read_sql("""SELECT * FROM orderDetails;""", conn)
print("------------------Order Details Data------------------")
print(order_details)
print("----------------End Order Details Data----------------")
Step 8
Find the total amount for all orders, calculated as the sum of rounded total prices, where the total price for each order is the priceEach multiplied by the quantityOrdered. Make sure you are rounding this internal product result.

Hint: Append .sum() to the end of your returned query that contains total price for each order, in order to create the total amount. You could also use the SUM() built-in SQL function as well.




For example:

sum_total = pd.read_sql("""
SELECT total_price
FROM some_table
""", conn).sum()
# STEP 8
# Replace None with your code
sum_total_price = None
Step 9
It is common in other parts of the world as well as the US Military to have dates as Day/Month/Year. Return the original order date column followed by three new columns that display the order date in this format with column names 'day', 'month', and 'year' respectively.

# STEP 9
# Replace None with your code
df_day_month_year = None
Close the connection
conn.close()