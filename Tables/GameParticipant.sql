-- ===============================
-- GameParticipant Table (Relationship Table)
-- Represents the many-to-many relationship between Game and Team
-- Stores which teams played in each game and their outcome
-- ===============================

CREATE TABLE GameParticipant (
    GameID INT NOT NULL, -- Foreign key: references a specific game
    TeamID INT NOT NULL, -- Foreign key: identifies the participating team
    PointsScored TINYINT NOT NULL, -- Total points scored by the team in the game
    IsWinner BOOLEAN NOT NULL, -- Indicates whether the team won (TRUE) or lost (FALSE)
    PRIMARY KEY (GameID, TeamID), -- Composite primary key: one entry per team per game
    FOREIGN KEY (GameID) REFERENCES Game(GameID), -- Ensures GameID exists in the Game table
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID) -- Ensures TeamID exists in the Team table
);