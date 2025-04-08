CREATE TABLE PlayerSeason (
    PlayerID INT NOT NULL,
    SeasonID INT NOT NULL,
    TeamID INT NOT NULL,
    Position VARCHAR(255) NOT NULL,   -- Here instead of Player (Could change via season or team)
    PlayerNumber INT,                 -- Jersey number for that team/season
    IsActive BOOLEAN DEFAULT TRUE,

    PRIMARY KEY (PlayerID, SeasonID),
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
    FOREIGN KEY (SeasonID) REFERENCES Season(SeasonID),
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID),
    CHECK (PlayerNumber > 0)
);