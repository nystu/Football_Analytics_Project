-- ===============================
-- TeamRoster Relationship Table for NFL Final Project
-- Connects Player, Team, and Season tables to track team membership, number, role, and physical stats for a specific season
-- ===============================

CREATE TABLE TeamRoster (
    RosterID INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each roster entry (auto-incremented)
    PlayerID INT NOT NULL, -- Foreign key: identifies the player
    TeamID INT NOT NULL, -- Foreign key: identifies the team
    SeasonID INT NOT NULL, -- Foreign key: identifies the season the player was on the roster
    JerseyNumber TINYINT, -- Player’s jersey number (1–99)
    Weight TINYINT NOT NULL, -- Player’s weight (in pounds, simplified to TINYINT for storage efficiency)
    Height TINYINT NOT NULL, -- Player’s height (in inches, e.g., 72 = 6 ft)
    Position VARCHAR(10) NOT NULL, -- Player’s position (e.g., QB, WR, LB)

    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID), -- Ensures the player exists in the Player table
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID), -- Ensures the team exists in the Team table
    FOREIGN KEY (SeasonID) REFERENCES Season(SeasonID), -- Ensures the season is valid
    CHECK (JerseyNumber BETWEEN 1 AND 99) -- Validates jersey numbers
);

-- ===============================================
-- Why Height, Weight, and Position are not in Player table:
-- These attributes can change from season to season or vary by team context.
-- For example:
--   - A player may gain/lose weight over time
--   - Their listed height may be updated as measured differently
--   - They may change positions or roles (e.g., WR to CB) between teams or seasons
-- Storing them in the TeamRoster table ensures season- and team-specific accuracy
-- without violating normalization principles (this maintains 3NF).
-- ===============================================