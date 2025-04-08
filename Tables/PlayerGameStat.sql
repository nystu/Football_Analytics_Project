CREATE TABLE PlayerGameStat (
    GameID INT NOT NULL,
    PlayerID INT NOT NULL,
    TeamID INT NOT NULL,  -- track the team the player played for in that game

    ReceivingTarget INT DEFAULT 0,
    Reception INT DEFAULT 0,
    ReceivingYard INT DEFAULT 0,
    ReceivingTD INT DEFAULT 0,

    PassingAttempt INT DEFAULT 0,
    PassingCompletion INT DEFAULT 0,
    PassingYard INT DEFAULT 0,
    PassingTD INT DEFAULT 0,
    ThrowInterception INT DEFAULT 0,

    RushingAttempt INT DEFAULT 0,
    RushingYard INT DEFAULT 0,
    RushingTD INT DEFAULT 0,

    Tackles INT DEFAULT 0,
    Sacks INT DEFAULT 0,
    Interceptions INT DEFAULT 0,

    FieldGoalAttempts INT DEFAULT 0,
    FieldGoalCompletions INT DEFAULT 0,
    ExtraPointAttempts INT DEFAULT 0,
    ExtraPointCompletions INT DEFAULT 0,

    PRIMARY KEY (GameID, PlayerID),
    FOREIGN KEY (GameID) REFERENCES Game(GameID), -- Game Player Played In
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID), -- Player we are Tracking
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID), -- Team for the Stats
    FOREIGN KEY (GameID, TeamID) REFERENCES PlaysIn(GameID, TeamID) 
		-- Ensures that the player’s team actually participated in the game
);