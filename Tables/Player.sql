-- ===============================
-- Player Table for NFL Final Project
-- Stores biographical information about each NFL player
-- ===============================

CREATE TABLE Player (
    PlayerID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for each player (auto-incremented)
    FirstName VARCHAR(50) NOT NULL, -- Player's first name
    LastName VARCHAR(50) NOT NULL, -- Player's last name
    BirthDate DATE NOT NULL, -- Date of birth in YYYY-MM-DD format
    College VARCHAR(255) NOT NULL, -- College the player attended
    UNIQUE (FirstName, LastName, BirthDate) -- Ensures no duplicate player by name and DOB
);