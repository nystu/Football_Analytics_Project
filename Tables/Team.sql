-- ===============================
-- Team Table for NFL Final Project
-- Stores details about each NFL team (unique identity, location, and grouping)
-- ===============================

CREATE TABLE Team (
    TeamID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for each team (auto-incremented)
    TeamName VARCHAR(50) NOT NULL UNIQUE, -- Full team name (e.g., 'Packers'), must be unique
    Location VARCHAR(50) NOT NULL, -- Geographic location of the team (e.g., 'Green Bay')
    Division VARCHAR(20), -- NFL division (e.g., 'North')
    Conference VARCHAR(20), -- NFL conference (e.g., 'NFC' or 'AFC')
    Abbreviation CHAR(3) NOT NULL UNIQUE -- Standard 3-letter team abbreviation (e.g., 'GB')
);

