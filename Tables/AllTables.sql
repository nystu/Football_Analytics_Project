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


-- ===============================
-- Team Table for NFL Final Project
-- Stores details about each NFL team (unique identity, location, and grouping)
-- ===============================
CREATE TABLE Team (
    TeamID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for each team (auto-incremented)
    TeamName VARCHAR(50) NOT NULL UNIQUE, -- Full team name (e.g., 'Packers'), must be unique
    Location VARCHAR(50) NOT NULL, -- Geographic location of the team (e.g., 'Green Bay')
    Division VARCHAR(20), -- NFL division (e.g., 'North')
    Conference VARCHAR(20), -- NFL conference (e.g., 'NFC' or 'AFC')
    Abbreviation CHAR(3) NOT NULL UNIQUE -- Standard 3-letter team abbreviation (e.g., 'GB')
);


-- ===============================
-- Player Table for NFL Final Project
-- Stores biographical information about each NFL player
-- ===============================
CREATE TABLE Player (
    PlayerID INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for each player (auto-incremented)
    FirstName VARCHAR(50) NOT NULL, -- Player's first name
    LastName VARCHAR(50) NOT NULL, -- Player's last name
    BirthDate DATE NOT NULL, -- Date of birth in YYYY-MM-DD format
    College VARCHAR(255) NOT NULL, -- College the player attended
	Weight SMALLINT NOT NULL, -- Player’s weight (in pounds, simplified to SMALLINT for storage efficiency)
    Height TINYINT NOT NULL, -- Player’s height (in inches, e.g., 72 = 6 ft)
    Position VARCHAR(10) NOT NULL, -- Player’s position (e.g., QB, WR, LB)
    UNIQUE (FirstName, LastName, BirthDate) -- Ensures no duplicate player by name and DOB
);


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






