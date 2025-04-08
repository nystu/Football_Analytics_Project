CREATE TABLE PlaysIn (
    GameID INT NOT NULL,
    TeamID INT NOT NULL,
    IsHome BOOLEAN NOT NULL,
    PointsScored INT NOT NULL,
    IsWinner BOOLEAN NOT NULL,
    PRIMARY KEY (GameID, TeamID),
    FOREIGN KEY (GameID) REFERENCES Game(GameID),
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID),
    CHECK (PointsScored >= 0)
);