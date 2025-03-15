import mysql.connector

# Database configuration
db_config = {
    'user': 'root',  # Replace with your MySQL username
    'password': 'catering@01',       # Your MySQL password
    'host': 'localhost',
}

# Connect to MySQL server
connection = mysql.connector.connect(**db_config)

# Create database and table
cursor = connection.cursor()

# Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS catering_portal")
cursor.execute("USE catering_portal")

# Create users table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
)
""")

# Insert a test user
cursor.execute("INSERT IGNORE INTO users (username, password) VALUES ('siddarda', 'reddy')")

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()

print("Database and table created successfully!")
