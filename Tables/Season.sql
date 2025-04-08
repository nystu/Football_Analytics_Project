CREATE TABLE Season (
    SeasonID INT NOT NULL, -- Example: 2223 (2022/2023)
    Description VARCHAR(255), -- e.g., '2023 Regular Season'
    StartDate DATE,
    EndDate DATE,
    IsPlayoffs BOOLEAN DEFAULT FALSE,  -- Optional
    PRIMARY KEY (SeasonID)
);