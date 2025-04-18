-- ===============================
-- GameStats Relationship Table for NFL Final Project
-- Connects Game, Player, and Team tables to store player-level statistics per game
-- ===============================

CREATE TABLE GameStats (
    GameStatID INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each stat entry (auto-incremented)
    GameID INT NOT NULL, -- Foreign key: identifies the game
    PlayerID INT NOT NULL, -- Foreign key: identifies the player
    TeamID INT NOT NULL, -- Foreign key: identifies the team the player was on during the game

    -- ===========================
    -- Offensive Stats
    -- ===========================
    
    -- Passing Offensive Stats
    PassingAttempts INT DEFAULT 0,
    PassingCompletions INT DEFAULT 0,
    PassingYards INT DEFAULT 0, -- Total passing yards
    PassingTDs TINYINT DEFAULT 0, -- Total passing touchdowns
    OffensiveInterceptions TINYINT DEFAULT 0, -- Interceptions thrown
    OffensiveFumbles TINYINT DEFAULT 0,
    
    -- Rushing Offensive Stats
    RushingAttempts INT DEFAULT 0,
    RushingYards INT DEFAULT 0, -- Total rushing yards
    RushingTDs TINYINT DEFAULT 0, -- Total rushing touchdowns
    
    -- Receiving Offensive Stats
    ReceivingYards INT DEFAULT 0, -- Total receiving yards
    ReceivingTDs TINYINT DEFAULT 0, -- Total receiving touchdowns
    Receptions TINYINT DEFAULT 0, -- Number of receptions

	-- ===========================
    -- Defensive Stats
    -- ===========================
    
    Tackles TINYINT DEFAULT 0, -- Number of tackles made
    Sacks DECIMAL(3,1) DEFAULT 0, -- Number of sacks (1 decimal point)
    ForcedFumbles TINYINT DEFAULT 0, -- Number of forced fumbles
    DefensiveInterceptions TINYINT DEFAULT 0, -- Defensive interceptions made
    DefensiveYards INT DEFAULT 0,
    DefensiveTDs TINYINT DEFAULT 0,

	-- ===========================
    -- Special Teams Stats
    -- ===========================
    
    FieldGoalsMade TINYINT DEFAULT 0, -- Field goals made
    FieldGoalsAttempted TINYINT DEFAULT 0, -- Field goals attempted
    ExtraPointsMade TINYINT DEFAULT 0, -- Extra points made
    ExtraPointsAttempted TINYINT DEFAULT 0, -- Extra points attempted
    PuntsAttempted TINYINT DEFAULT 0,
    PuntsYards INT DEFAULT 0,

    FOREIGN KEY (GameID) REFERENCES Game(GameID), -- Links to the Game table
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID), -- Links to the Player table
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID), -- Links to the Team table
    FOREIGN KEY (GameID, TeamID) REFERENCES GameParticipant(GameID, TeamID) -- Ensures player was on the participating team for that game
);