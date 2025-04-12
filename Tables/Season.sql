-- ===============================
-- Season Table for NFL Final Project
-- Stores information about each NFL season, including its time range
-- ===============================

CREATE TABLE Season (
    SeasonID INT PRIMARY KEY, -- Unique season identifier (e.g., 2324 for 2023–2024)
    Description VARCHAR(100), -- Human-readable label for the season
    StartDate DATE NOT NULL, -- Start date of the season (e.g., '2023-09-07')
    EndDate DATE NOT NULL -- End date of the season (e.g., '2024-02-11')
);