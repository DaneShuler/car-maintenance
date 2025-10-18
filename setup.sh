#!/bin/bash

# Function to display a message
display_message() {
    echo "=================================================="
    echo "$1"
    echo "=================================================="
}

# 1. Update the package manager
display_message "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Python3 and pip
display_message "Installing Python3 and pip..."
sudo apt-get install -y python3 python3-pip

# 3. Install MySQL server
display_message "Installing MySQL server..."
sudo apt-get install -y mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# 4. Install Python dependencies
display_message "Installing Python dependencies..."
pip3 install flask mysql-connector-python

# 5. Configure MySQL
display_message "Configuring MySQL..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS CarMaintenanceDB;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'your_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON CarMaintenanceDB.* TO 'root'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# 6. Set up the database schema
display_message "Setting up the database schema..."
mysql -u root -pyour_password CarMaintenanceDB < setup_database.sql

# 7. Final message
display_message "Setup is complete. Run the following command to start the Flask application:"
echo "python3 car_maintenance_web.py"
