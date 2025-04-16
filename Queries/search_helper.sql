-- Finds Offensive Stats for QB's
-- Calculates there totals for the whole season (including playoffs)
-- Computes there completion percentage and rounds 2 places
-- If PassingAttemps is zero then it is marked as null
SELECT 
    Player.FirstName,
    Player.LastName,
    Team.Location,
    SUM(GameStats.PassingAttempts) AS PassingAttempts,
    SUM(GameStats.PassingCompletions) AS PassingCompletions,
    SUM(GameStats.PassingYards) AS PassingYards,
	ROUND((SUM(GameStats.PassingCompletions) / NULLIF(SUM(GameStats.PassingAttempts), 0)) * 100, 2) AS CompletionPercentage
	FROM GameStats
		JOIN Player ON GameStats.PlayerID = Player.PlayerID
			JOIN Team ON GameStats.TeamID = Team.TeamID
	WHERE Player.Position = 'QB'
	GROUP BY Player.PlayerID, Team.TeamID
	ORDER BY PassingYards DESC, Player.LastName, Player.FirstName;


-- Need to Look at D.J. Moore and Amon-Ra St. Brown GameStats
SELECT 
    Player.FirstName,
    Player.LastName,
    MIN(Team.Location),
    SUM(GameStats.ReceivingYards),
    SUM(GameStats.Receptions),
    ROUND(SUM(GameStats.ReceivingYards) / NULLIF(SUM(GameStats.Receptions), 0), 2)
	FROM GameStats
		JOIN Player ON GameStats.PlayerID = Player.PlayerID
			JOIN Team ON GameStats.TeamID = Team.TeamID
	WHERE Player.Position = 'WR'
	GROUP BY Player.PlayerID
	ORDER BY SUM(GameStats.ReceivingYards) DESC, Player.LastName, Player.FirstName;


-- Top 10 most productive WRs by receiving yards per reception
-- They Need to HAVE a minumum of 100 Receptions
-- Sum up all stats for this player while they were on this specific team.
SELECT 
    Player.FirstName,
    Player.LastName,
    Team.Location,
    SUM(GameStats.ReceivingYards) AS Yards,
    SUM(GameStats.Receptions) AS Receptions,
    ROUND(SUM(GameStats.ReceivingYards) / NULLIF(SUM(GameStats.Receptions), 0), 2) AS YardsPerReception
	FROM GameStats
		JOIN Player ON GameStats.PlayerID = Player.PlayerID
			JOIN Team ON GameStats.TeamID = Team.TeamID
	WHERE Player.Position = 'WR'
	GROUP BY Player.PlayerID, Team.TeamID
	HAVING Receptions >= 100
	ORDER BY YardsPerReception DESC
	LIMIT 10;
    
SELECT *
	FROM GameStats
	WHERE PlayerID = 701;
        
	
SELECT *
	FROM Player;




