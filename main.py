# STEP 1A
# Import SQL Library
import sqlite3

# STEP 1B
# Connect to the database
conn = sqlite3.connect('data.sqlite')

# Example to see all employee data
cursor = conn.cursor()
employee_data = cursor.execute("""SELECT * FROM employees""").fetchall()
print("---------------------Employee Data---------------------")
for row in employee_data:
    print(row)
print("-------------------End Employee Data-------------------")

# STEP 2
# Get employee number and last name
df_first_five = conn.cursor().execute("""
    SELECT employeeNumber, lastName
    FROM employees
""").fetchall()
print("------------------Employee Number and Last Name------------------")
for row in df_first_five:
    print(row)
print("-------------------End Employee Number and Last Name-------------------")

# STEP 3
# Same thing but with reversed column order
df_five_reverse = conn.cursor().execute("""
    SELECT lastName, employeeNumber
    FROM employees
""").fetchall()
print("------------------Last Name and Employee Number (Reversed)------------------")
for row in df_five_reverse:
    print(row)
print("-------------------End Last Name and Employee Number (Reversed)-------------------")

# STEP 4
# Rename employeeNumber to ID using alias
df_alias = conn.cursor().execute("""
    SELECT lastName, employeeNumber AS ID
    FROM employees
""").fetchall()
print("------------------Last Name and ID (Alias)------------------")
for row in df_alias:
    print(row)
print("-------------------End Last Name and ID (Alias)-------------------")

# STEP 5
# Categorize employees by role (Executive vs Not Executive)
df_executive = conn.cursor().execute("""
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
""").fetchall()
print("------------------Employee Role Categorization------------------")
for row in df_executive:
    print(row)
print("-------------------End Employee Role Categorization-------------------")

# STEP 6
# Get length of last names
df_name_length = conn.cursor().execute("""
    SELECT LENGTH(lastName) AS name_length
    FROM employees
""").fetchall()
print("------------------Length of Last Names------------------")
for row in df_name_length:
    print(row)
print("-------------------End Length of Last Names-------------------")

# STEP 7
# Get first 2 letters of job titles
df_short_title = conn.cursor().execute("""
    SELECT SUBSTR(jobTitle, 1, 2) AS short_title
    FROM employees
""").fetchall()
print("------------------First 2 Letters of Job Titles------------------")
for row in df_short_title:
    print(row)
print("-------------------End First 2 Letters of Job Titles-------------------")

# Add the code below and run the file to see order details data
order_details = conn.cursor().execute("""SELECT * FROM orderDetails;""").fetchall()
print("------------------Order Details Data------------------")
for row in order_details:
    print(row)
print("----------------End Order Details Data----------------")

# STEP 8
# Calculate total of all orders (price * quantity, rounded)
cursor = conn.cursor()
cursor.execute("""
    SELECT SUM(ROUND(priceEach * quantityOrdered)) as total
    FROM orderDetails
""")
sum_total_price = cursor.fetchone()[0]
print("------------------Total of All Orders------------------")
print(f"Total: {sum_total_price}")
print("-------------------End Total-------------------")

# STEP 9
# Parse dates into day, month, year columns
df_day_month_year = conn.cursor().execute("""
    SELECT
        orderDate,
        SUBSTR(orderDate, 9, 2) AS day,
        SUBSTR(orderDate, 6, 2) AS month,
        SUBSTR(orderDate, 1, 4) AS year
    FROM orders
""").fetchall()
print("------------------Order Date Parts------------------")
for row in df_day_month_year:
    print(row)
print("-------------------End Date Parts-------------------")

# Close connection
conn.close()
