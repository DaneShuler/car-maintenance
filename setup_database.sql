-- Create Database
CREATE DATABASE CarMaintenanceDB;
USE CarMaintenanceDB;

-- Create Tables
CREATE TABLE Vehicle (
    VehicleID INT AUTO_INCREMENT PRIMARY KEY,
    Make VARCHAR(50),
    Model VARCHAR(50),
    Year INT,
    VIN VARCHAR(17) UNIQUE
);

CREATE TABLE Maintenance (
    MaintenanceID INT AUTO_INCREMENT PRIMARY KEY,
    VehicleID INT,
    DateOfService DATE,
    TypeOfService VARCHAR(100),
    Mileage INT,
    NextServiceDate DATE,
    NextServiceMileage INT,
    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID) ON DELETE CASCADE
);

CREATE TABLE PartsInventory (
    PartID INT AUTO_INCREMENT PRIMARY KEY,
    PartName VARCHAR(100),
    Quantity INT,
    VehicleID INT NULL,
    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID) ON DELETE SET NULL
);

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE,
    Password VARCHAR(255),
    Role ENUM('Admin', 'User')
);

-- Populate Tables with Sample Data
INSERT INTO Vehicle (Make, Model, Year, VIN)
VALUES 
('Toyota', 'Corolla', 2018, 'JTDBU4EE9A1234567'),
('Chevy', 'Corvette', 2008, '1G1YY25W285124928'),
('Honda', 'Civic', 2020, '2HGFC2F6XH1234568'),
('Ford', 'F-150', 2015, '1FTFW1EF1FKD84332'),
('BMW', 'X5', 2021, '5UXCR6C09M9H12345'),
('Tesla', 'Model S', 2022, '5YJSA1E22JF123456'),
('Toyota', 'Camry', 2019, '4T1B11HK6KU123456'),
('Chevy', 'Silverado', 2020, '1GCPYBEH1LZ123456'),
('Honda', 'Accord', 2021, '1HGCV1F37MA123456'),
('Ford', 'Mustang', 2017, '1FA6P8CF6H5301234'),
('BMW', '3 Series', 2020, 'WBA8D9C56KA123456'),
('Tesla', 'Model 3', 2022, '5YJ3E1EB9JF123456'),
('Nissan', 'Altima', 2016, '1N4BL3AP8GC123456'),
('Jeep', 'Wrangler', 2018, '1C4HJXEG5JW123456'),
('Mazda', 'CX-5', 2021, 'JM3KFBDM2M1234567'),
('Subaru', 'Outback', 2020, '4S4BRCAC3L3123456'),
('Hyundai', 'Elantra', 2019, 'KMHD04LB1KU123456'),
('Kia', 'Sorento', 2022, '5XYRKDLF6LG123456'),
('Volkswagen', 'Passat', 2018, '1VWAT7A36JC123456'),
('Audi', 'A4', 2021, 'WAUENAF49KA123456'),
('Chevy', 'Impala', 2017, '2G1125S31H1234567'),
('Toyota', 'Highlander', 2020, '5TDZZRFH5LS123456'),
('Honda', 'CR-V', 2021, '2HKRW2H86MH123456'),
('Ford', 'Explorer', 2022, '1FM5K8D82NGA12345'),
('BMW', 'M5', 2022, 'WBSFV9C54ND123456');


INSERT INTO Maintenance (VehicleID, DateOfService, TypeOfService, Mileage, NextServiceDate, NextServiceMileage)
VALUES
(1, '2023-10-01', 'Oil Change', 10000, '2024-01-01', 12000),
(2, '2023-09-15', 'Brake Replacement', 15000, '2024-02-15', 20000),
(3, '2023-07-10', 'Battery Replacement', 25000, '2024-07-10', NULL),
(4, '2023-10-20', 'Transmission Service', 80000, '2024-10-20', 90000),
(5, '2023-11-01', 'Oil Change', 5000, '2024-02-01', 10000),
(6, '2023-11-05', 'Software Update', 1200, '2024-03-05', NULL),
(7, '2023-08-01', 'Brake Fluid Replacement', 30000, '2024-02-01', 35000),
(8, '2023-07-20', 'Tire Rotation', 15000, '2024-01-20', 20000),
(9, '2023-06-15', 'Oil Change', 20000, '2024-06-15', 30000),
(10, '2023-09-01', 'Air Filter Replacement', 18000, '2024-03-01', 25000),
(11, '2023-10-11', 'Coolant Flush', 50000, '2024-10-11', 60000),
(12, '2023-09-25', 'Tire Replacement', 40000, '2024-09-25', 50000),
(13, '2023-10-05', 'Brake Pad Replacement', 30000, '2024-04-05', 40000),
(14, '2023-11-01', 'Spark Plug Replacement', 60000, '2024-11-01', 70000),
(15, '2023-12-01', 'Oil Change', 10000, '2024-03-01', 20000),
(16, '2023-07-01', 'Fuel Filter Replacement', 50000, '2024-07-01', 60000),
(17, '2023-06-01', 'Suspension Inspection', 75000, '2024-06-01', NULL),
(18, '2023-05-01', 'Battery Replacement', 45000, '2024-05-01', 55000),
(19, '2023-04-01', 'Transmission Service', 85000, '2024-04-01', 95000),
(20, '2023-03-01', 'Timing Belt Replacement', 90000, '2024-03-01', NULL),
(21, '2023-02-01', 'Brake Rotor Replacement', 95000, '2024-02-01', 105000),
(22, '2023-01-01', 'Windshield Wiper Replacement', 5000, '2024-01-01', NULL),
(23, '2022-12-01', 'Battery Check', 15000, '2023-12-01', NULL),
(24, '2022-11-01', 'Oil Change', 3000, '2023-02-01', 5000),
(25, '2022-10-01', 'Cabin Air Filter Replacement', 10000, '2023-10-01', 20000);


INSERT INTO PartsInventory (PartName, Quantity, VehicleID)
VALUES
('Air Filter', 50, 1),
('Brake Pads', 30, 2),
('Oil Filter', 25, 3),
('Tires', 10, 4),
('Spark Plugs', 100, 5),
('Wiper Blades', 20, 6),
('Battery', 15, 7),
('Transmission Fluid', 40, 8),
('Coolant', 60, 9),
('Fuel Filter', 30, 10),
('Brake Rotors', 20, 11),
('Timing Belt', 10, 12),
('Suspension Kit', 5, 13),
('Cabin Air Filter', 25, 14),
('Headlight Bulbs', 15, 15),
('Windshield Washer Fluid', 50, 16),
('Alternator', 10, 17),
('Radiator', 5, 18),
('Oil Pan', 10, 19),
('Starter Motor', 15, 20),
('Clutch Kit', 10, 21),
('Catalytic Converter', 5, 22),
('Exhaust System', 5, 23),
('Turbocharger', 3, 24),
('Supercharger', 2, 25);


INSERT INTO Users (Username, Password, Role)
VALUES
('admin', 'adminpassword', 'Admin'),
('user1', 'userpassword1', 'User'),
('mechanic_john', 'securepass123', 'Admin'),
('shop_owner', 'shopsecure456', 'Admin'),
('customer_anna', 'annapass789', 'User'),
('user2', 'password123', 'User'),
('admin_jane', 'admin12345', 'Admin'),
('service_manager', 'managersecure', 'Admin'),
('repair_guy', 'repair1234', 'User'),
('mechanic_sam', 'password4321', 'Admin'),
('customer_tom', 'tom123pass', 'User'),
('user_bob', 'bobsecurepass', 'User'),
('admin_sara', 'sarapassadmin', 'Admin'),
('user_emily', 'emilysecure1', 'User'),
('customer_jake', 'jake123', 'User'),
('mechanic_kim', 'kimsecurepass', 'Admin'),
('shop_helper', 'helper12345', 'User'),
('user_max', 'maxpassword', 'User'),
('admin_lisa', 'lisapassadmin', 'Admin'),
('manager_kate', 'katepassword', 'Admin'),
('technician_mike', 'mikepass123', 'User'),
('customer_steve', 'steve123', 'User'),
('repair_bob', 'repair456', 'User'),
('admin_harry', 'harrysecurepass', 'Admin'),
('customer_linda', 'lindapass789', 'User');

