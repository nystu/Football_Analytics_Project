-- ===============================
-- Game Table for NFL Final Project
-- Stores details about each NFL game, linked to seasons and teams
-- ===============================

CREATE TABLE Game (
    GameID INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each game (auto-incremented)
    SeasonID INT NOT NULL, -- Foreign key: links game to a specific season
    GameWeek TINYINT NOT NULL, -- Week number of the game (1–18 for regular season, 19+ for playoffs)
    GameDay VARCHAR(20), -- Day of the week (e.g., 'Sunday', 'Monday') – optional but useful for frontend displays
    GameDate DATE NOT NULL, -- Exact date of the game (e.g., '2024-10-15')
    GameTime TIME NOT NULL, -- Kickoff time (24-hr format, e.g., '13:00:00')
    SeasonType ENUM('Preseason', 'Regular', 'Postseason') NOT NULL, -- Categorizes each game by season phase
    HomeTeamID INT NOT NULL, -- Foreign key: references the team hosting the game
    AwayTeamID INT NOT NULL, -- Foreign key: references the visiting team
    FOREIGN KEY (SeasonID) REFERENCES Season(SeasonID), -- Ensures SeasonID exists in the Season table
    FOREIGN KEY (HomeTeamID) REFERENCES Team(TeamID), -- Ensures HomeTeamID is a valid team
    FOREIGN KEY (AwayTeamID) REFERENCES Team(TeamID), -- Ensures AwayTeamID is a valid team
    CHECK (HomeTeamID <> AwayTeamID), -- Prevents a team from playing itself
    UNIQUE (SeasonID, GameWeek, HomeTeamID, AwayTeamID) -- Ensures no duplicate game records per season and week
);