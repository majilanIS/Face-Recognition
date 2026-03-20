from database import get_connection

conn = get_connection()
if conn:
    print("Connection successful!")
else:
    print("Connection failed.")

