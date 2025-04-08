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

ALTER TABLE Game
	CHANGE Season SeasonID INT NOT NULL;

ALTER TABLE Game
	ADD CONSTRAINT fk_game_season
	FOREIGN KEY (SeasonID) REFERENCES Season(SeasonID);

-- New Games Table:
-- Game(
--     GameID INT AUTO_INCREMENT PRIMARY KEY,     -- Unique game ID
--     GameDate DATE NOT NULL,                    -- Date of the game
--     SeasonID INT NOT NULL,                     -- Foreign key to Season table
--     Week INT NOT NULL,                         -- Week number in the season
--     HomeScore INT NOT NULL CHECK (HomeScore >= 0),  -- Score for the home team
--     AwayScore INT NOT NULL CHECK (AwayScore >= 0),  -- Score for the away team
--     FOREIGN KEY (SeasonID) REFERENCES Season(SeasonID)  -- Link to Season
-- )

