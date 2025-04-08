CREATE TABLE Team (
    TeamID INT NOT NULL AUTO_INCREMENT,
    TeamName VARCHAR(255) NOT NULL,
    TeamLocation VARCHAR(255) NOT NULL,
    TeamDivision VARCHAR(255) NOT NULL,
    TeamConference VARCHAR(255) NOT NULL,
    PRIMARY KEY (TeamID)
);

INSERT INTO Team (TeamName, TeamLocation, TeamDivision, TeamConference) VALUES
	('Cardinals', 'Arizona', 'NFC West', 'NFC'),
	('Falcons', 'Atlanta', 'NFC South', 'NFC'),
	('Ravens', 'Baltimore', 'AFC North', 'AFC'),
	('Bills', 'Buffalo', 'AFC East', 'AFC'),
	('Panthers', 'Carolina', 'NFC South', 'NFC'),
	('Bears', 'Chicago', 'NFC North', 'NFC'),
	('Bengals', 'Cincinnati', 'AFC North', 'AFC'),
	('Browns', 'Cleveland', 'AFC North', 'AFC'),
	('Cowboys', 'Dallas', 'NFC East', 'NFC'),
	('Broncos', 'Denver', 'AFC West', 'AFC'),
	('Lions', 'Detroit', 'NFC North', 'NFC'),
	('Packers', 'Green Bay', 'NFC North', 'NFC'),
	('Texans', 'Houston', 'AFC South', 'AFC'),
	('Colts', 'Indianapolis', 'AFC South', 'AFC'),
	('Jaguars', 'Jacksonville', 'AFC South', 'AFC'),
	('Chiefs', 'Kansas City', 'AFC West', 'AFC'),
	('Raiders', 'Las Vegas', 'AFC West', 'AFC'),
	('Chargers', 'Los Angeles', 'AFC West', 'AFC'),
	('Rams', 'Los Angeles', 'NFC West', 'NFC'),
	('Dolphins', 'Miami', 'AFC East', 'AFC'),
	('Vikings', 'Minnesota', 'NFC North', 'NFC'),
	('Patriots', 'New England', 'AFC East', 'AFC'),
	('Saints', 'New Orleans', 'NFC South', 'NFC'),
	('Giants', 'New York', 'NFC East', 'NFC'),
	('Jets', 'New York', 'AFC East', 'AFC'),
	('Eagles', 'Philadelphia', 'NFC East', 'NFC'),
	('Steelers', 'Pittsburgh', 'AFC North', 'AFC'),
	('49ers', 'San Francisco', 'NFC West', 'NFC'),
	('Seahawks', 'Seattle', 'NFC West', 'NFC'),
	('Buccaneers', 'Tampa Bay', 'NFC South', 'NFC'),
	('Titans', 'Tennessee', 'AFC South', 'AFC'),
	('Commanders', 'Washington', 'NFC East', 'NFC');
    
SELECT TeamID, TeamName, TeamLocation, TeamDivision, TeamConference
	FROM Team
	ORDER BY TeamConference, TeamDivision;
    
