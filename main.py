# STEP 1A
# Import SQL Library and Pandas
import sqlite3
import pandas as pd

# STEP 1B
# Connect to the database
conn = sqlite3.connect('data.sqlite')

# Example to see all employee data
employee_data = pd.read_sql("""SELECT * FROM employees""", conn)
print("---------------------Employee Data---------------------")
print(employee_data)
print("-------------------End Employee Data-------------------")

# STEP 2
# Get employee number and last name
df_first_five = pd.read_sql("""
    SELECT employeeNumber, lastName 
    FROM employees
""", conn)

# STEP 3
# Same thing but with reversed column order
df_five_reverse = pd.read_sql("""
    SELECT lastName, employeeNumber 
    FROM employees
""", conn)

# STEP 4
# Rename employeeNumber to ID using alias
df_alias = pd.read_sql("""
    SELECT lastName, employeeNumber AS ID 
    FROM employees
""", conn)

# STEP 5
# Categorize employees by role (Executive vs Not Executive)
df_executive = pd.read_sql("""
    SELECT 
        employeeNumber,
        lastName,
        firstName,
        jobTitle,
        CASE 
            WHEN jobTitle = 'President' OR jobTitle = 'VP Sales' OR jobTitle = 'VP Marketing' 
            THEN 'Executive' 
            ELSE 'Not Executive' 
        END AS role
    FROM employees
""", conn)

# STEP 6
# Get length of last names
df_name_length = pd.read_sql("""
    SELECT LENGTH(lastName) AS name_length
    FROM employees
""", conn)

# STEP 7
# Get first 2 letters of job titles
df_short_title = pd.read_sql("""
    SELECT SUBSTR(jobTitle, 1, 2) AS short_title
    FROM employees
""", conn)

# Add the code below and run the file to see order details data
order_details = pd.read_sql("""SELECT * FROM orderDetails;""", conn)
print("------------------Order Details Data------------------")
print(order_details)
print("----------------End Order Details Data----------------")

# STEP 8
# Calculate total of all orders (price * quantity, rounded)
sum_total_price = pd.read_sql("""
    SELECT SUM(ROUND(priceEach * quantityOrdered)) as total
    FROM orderDetails
""", conn).iloc[0].values

# STEP 9
# Parse dates into day, month, year columns
df_day_month_year = pd.read_sql("""
    SELECT 
        orderDate,
        SUBSTR(orderDate, 9, 2) AS day,
        SUBSTR(orderDate, 6, 2) AS month,
        SUBSTR(orderDate, 1, 4) AS year
    FROM orders
""", conn)

# Close connection
conn.close()
