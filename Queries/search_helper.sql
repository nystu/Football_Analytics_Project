SELECT *	
	FROM Team;

SELECT *
	FROM GameStats;

SELECT *
	FROM Game G
		LEFT JOIN GameStats GS ON G.GameID = GS.GameID
	WHERE GS.GameID IS NULL;

SELECT 
    P.PlayerID,
    P.FirstName,
    P.LastName,
    T.TeamName,
    MIN(G.GameDate) AS FirstGameDate,
    MAX(G.GameDate) AS LastGameDate
FROM GameStats GS
JOIN Game G ON GS.GameID = G.GameID
JOIN Player P ON GS.PlayerID = P.PlayerID
JOIN Team T ON GS.TeamID = T.TeamID
WHERE G.SeasonID = 2425
GROUP BY GS.PlayerID, GS.TeamID
HAVING COUNT(DISTINCT GS.TeamID) >= 1
AND GS.PlayerID IN (
    SELECT GS2.PlayerID
    FROM GameStats GS2
    GROUP BY GS2.PlayerID
    HAVING COUNT(DISTINCT GS2.TeamID) > 1
)
ORDER BY P.PlayerID, FirstGameDate;

    
    
     
-- DELETE FROM GameStats WHERE GameStatID >=0;
-- ALTER TABLE GameStats AUTO_INCREMENT = 1;



-- '1','Cardinals','Arizona','West','NFC','ARI'
-- '2','Falcons','Atlanta','South','NFC','ATL'
-- '3','Ravens','Baltimore','North','AFC','BAL'
-- '4','Bills','Buffalo','East','AFC','BUF'
-- '5','Panthers','Carolina','South','NFC','CAR'
-- '6','Bears','Chicago','North','NFC','CHI'
-- '7','Bengals','Cincinnati','North','AFC','CIN'
-- '8','Browns','Cleveland','North','AFC','CLE'
-- '9','Cowboys','Dallas','East','NFC','DAL'
-- '10','Broncos','Denver','West','AFC','DEN'
-- '11','Lions','Detroit','North','NFC','DET'
-- '12','Packers','Green Bay','North','NFC','GNB'
-- '13','Texans','Houston','South','AFC','HOU'
-- '14','Colts','Indianapolis','South','AFC','IND'
-- '15','Jaguars','Jacksonville','South','AFC','JAX'
-- '16','Chiefs','Kansas City','West','AFC','KAN'
-- '17','Raiders','Las Vegas','West','AFC','LVR'
-- '18','Chargers','Los Angeles','West','AFC','LAC'
-- '19','Rams','Los Angeles','West','NFC','LAR'
-- '20','Dolphins','Miami','East','AFC','MIA'
-- '21','Vikings','Minnesota','North','NFC','MIN'
-- '22','Patriots','New England','East','AFC','NWE'
-- '23','Saints','New Orleans','South','NFC','NOR'
-- '24','Giants','New York','East','NFC','NYG'
-- '25','Jets','New York','East','AFC','NYJ'
-- '26','Eagles','Philadelphia','East','NFC','PHI'
-- '27','Steelers','Pittsburgh','North','AFC','PIT'
-- '28','49ers','San Francisco','West','NFC','SFO'
-- '29','Seahawks','Seattle','West','NFC','SEA'
-- '30','Buccaneers','Tampa Bay','South','NFC','TAM'
-- '31','Titans','Tennessee','South','AFC','TEN'
-- '32','Commanders','Washington','East','NFC','WAS'
