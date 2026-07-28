import mysql.connector
from config import *

print("db.py is running...")

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    if connection.is_connected():
        print("✅ Connected to MySQL Successfully!")

except mysql.connector.Error as err:
    print("❌ Error:", err)