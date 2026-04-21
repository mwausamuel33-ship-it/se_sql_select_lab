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

# STEP 3
# Same thing but with reversed column order
df_five_reverse = conn.cursor().execute("""
    SELECT lastName, employeeNumber
    FROM employees
""").fetchall()

# STEP 4
# Rename employeeNumber to ID using alias
df_alias = conn.cursor().execute("""
    SELECT lastName, employeeNumber AS ID
    FROM employees
""").fetchall()

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

# STEP 6
# Get length of last names
df_name_length = conn.cursor().execute("""
    SELECT LENGTH(lastName) AS name_length
    FROM employees
""").fetchall()

# STEP 7
# Get first 2 letters of job titles
df_short_title = conn.cursor().execute("""
    SELECT SUBSTR(jobTitle, 1, 2) AS short_title
    FROM employees
""").fetchall()

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

# Close connection
conn.close()
