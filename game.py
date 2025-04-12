import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector

# --- Config ---
SEASON_ID = 2324
URL = "https://www.pro-football-reference.com/years/2024/games.htm"
CAPTION_TEXT = "Week-by-Week Regular Season and Preseason Games Table"

TEAM_NAME_TO_ABBR = {
    'Arizona Cardinals': 'ARZ', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BLT', 'Buffalo Bills': 'BUF',
    'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLV',
    'Dallas Cowboys': 'DAL', 'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB',
    'Houston Texans': 'HST', 'Indianapolis Colts': 'IND', 'Jacksonville Jaguars': 'JAX', 'Kansas City Chiefs': 'KC',
    'Las Vegas Raiders': 'LV', 'Los Angeles Chargers': 'LAC', 'Los Angeles Rams': 'LA', 'Miami Dolphins': 'MIA',
    'Minnesota Vikings': 'MIN', 'New England Patriots': 'NE', 'New Orleans Saints': 'NO', 'New York Giants': 'NYG',
    'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 'Pittsburgh Steelers': 'PIT', 'San Francisco 49ers': 'SF',
    'Seattle Seahawks': 'SEA', 'Tampa Bay Buccaneers': 'TB', 'Tennessee Titans': 'TEN', 'Washington Commanders': 'WAS'
}

WEEK_LABELS = {
    'WildCard': 19,
    'Division': 20,
    'ConfChamp': 21,
    'SuperBowl': 22
}

# --- MySQL Connect ---
conn = mysql.connector.connect(
    host="138.49.184.47",
    port=3306,
    user="nystuen6918",
    password="MdSDU6V2!g3aNZxb",
    database="nystuen6918_FA_Project"
)
cursor = conn.cursor()

# --- Load and Parse HTML ---
print(f"Fetching schedule from: {URL}")
html = requests.get(URL).text
soup = BeautifulSoup(html, "html.parser")

# --- Locate the table by caption ---
caption = soup.find("caption", string=CAPTION_TEXT)
if not caption:
    print("❌ Could not find caption with schedule table.")
    exit()

table = caption.find_parent("table")
if not table:
    print("❌ Could not find schedule table element.")
    exit()

print("✅ Schedule table found.")

rows = table.find("tbody").find_all("tr")
inserted = 0

for row in rows:
    if 'thead' in row.get('class', []):
        continue

    cols = row.find_all("td")
    if len(cols) < 10:
        continue

    week_raw = row.find("th").text.strip()
    game_day = cols[0].text.strip()
    game_date_raw = cols[1].text.strip()
    game_time_raw = cols[2].text.strip()
    winner = cols[3].text.strip()
    at_symbol = cols[4].text.strip()
    loser = cols[5].text.strip()
    winner_score_raw = cols[7].text.strip()
    loser_score_raw = cols[8].text.strip()

    # Week logic
    if week_raw.isdigit():
        week = int(week_raw)
    else:
        week = WEEK_LABELS.get(week_raw.replace(" ", ""))
        if not week:
            print(f"⚠️ Unknown week label: {week_raw}")
            continue

    season_type = 'Postseason' if week >= 18 else 'Regular'

    try:
        game_date = datetime.strptime(game_date_raw, "%Y-%m-%d").date()
        game_time = datetime.strptime(game_time_raw, "%I:%M%p").time()
    except Exception as e:
        print(f"⚠️ Error parsing datetime: {e}")
        continue

    winner_abbr = TEAM_NAME_TO_ABBR.get(winner)
    loser_abbr = TEAM_NAME_TO_ABBR.get(loser)

    if not winner_abbr or not loser_abbr:
        print(f"⚠️ Unknown team abbreviation: {winner} / {loser}")
        continue

    cursor.execute("SELECT TeamID FROM Team WHERE Abbreviation = %s", (winner_abbr,))
    winner_team_id = cursor.fetchone()
    cursor.execute("SELECT TeamID FROM Team WHERE Abbreviation = %s", (loser_abbr,))
    loser_team_id = cursor.fetchone()

    if not winner_team_id or not loser_team_id:
        print(f"⚠️ Missing TeamIDs for {winner} or {loser}")
        continue

    winner_team_id = winner_team_id[0]
    loser_team_id = loser_team_id[0]

    home_team_id = loser_team_id if at_symbol == '@' else winner_team_id
    away_team_id = winner_team_id if at_symbol == '@' else loser_team_id

    # Duplicate check
    cursor.execute("""
        SELECT GameID FROM Game
        WHERE SeasonID = %s AND GameWeek = %s AND HomeTeamID = %s AND AwayTeamID = %s
    """, (SEASON_ID, week, home_team_id, away_team_id))
    if cursor.fetchone():
        print(f"⏭️ Duplicate game: Week {week} {winner} vs {loser}")
        continue

    # Insert into Game
    cursor.execute("""
        INSERT INTO Game (
            SeasonID, GameWeek, GameDay, GameDate, GameTime,
            SeasonType, HomeTeamID, AwayTeamID
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        SEASON_ID, week, game_day, game_date, game_time,
        season_type, home_team_id, away_team_id
    ))
    game_id = cursor.lastrowid

    try:
        winner_score = int(winner_score_raw)
        loser_score = int(loser_score_raw)
    except ValueError:
        print(f"⚠️ Invalid score: {winner_score_raw} or {loser_score_raw}")
        continue

    # Insert into GameParticipant
    cursor.execute("""
        INSERT INTO GameParticipant (GameID, TeamID, PointsScored, IsWinner)
        VALUES (%s, %s, %s, TRUE)
    """, (game_id, winner_team_id, winner_score))

    cursor.execute("""
        INSERT INTO GameParticipant (GameID, TeamID, PointsScored, IsWinner)
        VALUES (%s, %s, %s, FALSE)
    """, (game_id, loser_team_id, loser_score))

    inserted += 1
    print(f"✅ Inserted Week {week} ({season_type}): {winner} vs {loser}")

# Finalize
conn.commit()
cursor.close()
conn.close()
print(f"\n🎉 Done! Inserted {inserted} games and GameParticipant rows.")