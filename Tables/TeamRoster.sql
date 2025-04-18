-- ===============================
-- TeamRoster Relationship Table for NFL Final Project
-- Connects Player, Team, and Season tables to track team membership, number, role, and physical stats for a specific season
-- ===============================

CREATE TABLE TeamRoster (
    RosterID INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each roster entry (auto-incremented)
    PlayerID INT NOT NULL, -- Foreign key: identifies the player
    TeamID INT NOT NULL, -- Foreign key: identifies the team
    SeasonID INT NOT NULL, -- Foreign key: identifies the season the player was on the roster
	StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    JerseyNumber TINYINT, -- Player’s jersey number (1–99)
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID), -- Ensures the player exists in the Player table
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID), -- Ensures the team exists in the Team table
    FOREIGN KEY (SeasonID) REFERENCES Season(SeasonID), -- Ensures the season is valid
    CHECK (JerseyNumber BETWEEN 1 AND 99) -- Validates jersey numbers
);
