PRAGMA foreign_keys = ON;



CREATE TABLE IF NOT EXISTS Product (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Name VARCHAR(50) NOT NULL,
    Cost DECIMAL(10,2) NOT NULL,
    Description TEXT,
    Specification TEXT,
    Label VARCHAR(20) NOT NULL,
    BrandID INTEGER NOT NULL,
    FOREIGN KEY (BrandID) REFERENCES Brand (ID) ON DELETE CASCADE
)

CREATE TABLE IF NOT EXISTS Brand (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Name VARCHAR(50) NOT NULL
)


CREATE TABLE IF NOT EXISTS Booking (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    -- In Complete version would use encryption at rest for storing identifiable information
    Name VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Tel VARCHAR(12) NUMERIC NOT NULL,
    Date DATE NOT NULL,
    Time VARCHAR(5),
    AccountID INTEGER,
    FOREIGN KEY (AccountID) REFERENCES Account(ID)
)

CREATE TABLE IF NOT EXISTS Account (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Username VARCHAR(50) NOT NULL,
    -- Use Python bcrypt to hash passwords before store
    Password VARCHAR(100) NOT NULL
)