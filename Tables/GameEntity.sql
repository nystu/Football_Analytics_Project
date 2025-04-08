CREATE TABLE Game (
    GameID INT NOT NULL AUTO_INCREMENT,
    GameDate DATE NOT NULL,
    Season INT NOT NULL,
    Week INT NOT NULL,
    HomeScore INT NOT NULL,
    AwayScore INT NOT NULL,
    PRIMARY KEY (GameID),
    CHECK (HomeScore >= 0),
    CHECK (AwayScore >= 0)
);