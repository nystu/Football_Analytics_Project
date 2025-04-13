import requests # Fetches the HTML content from the specified URL
from bs4 import BeautifulSoup # Parses the HTML content and allows us to navigate and search through it
from datetime import datetime # Handles date and time parsing
import mysql.connector # Connects to the MySQL database using the mysql-connector-python library



# --- Configuration of Constants ---
# SEASON_ID: The ID of the season for which the games are being inserted.
# URL: The URL of the webpage containing the schedule.
# CAPTION_TEXT: The text of the caption that identifies the schedule table in the HTML.
# TEAM_NAME_TO_ABBR: A dictionary mapping full team names to their abbreviations.
# WEEK_LABELS: A dictionary mapping special week labels (like WildCard, Division, etc.) to their corresponding week numbers.
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
    'SuperBowl': 22,
}



# --- MySQL Connect ---
# Connects to the MySQL database using the mysql-connector-python library.
# Make sure to install it using pip if you haven't already:
# pip install mysql-connector-python
# Replace with your actual database connection details
conn = mysql.connector.connect(
    host="138.49.184.47",
    port=3306,
    user="nystuen6918",
    password="MdSDU6V2!g3aNZxb",
    database="nystuen6918_FA_Project"
)
cursor = conn.cursor()



# --- Load and Parse HTML ---
# requests.get() fetches the HTML content from the specified URL.
# BeautifulSoup parses the HTML content and allows us to navigate and search through it.
# Make sure to install BeautifulSoup4 if you haven't already:
# pip install beautifulsoup4
print(f"Fetching schedule from: {URL}")
html = requests.get(URL).text
soup = BeautifulSoup(html, "html.parser")



# --- Locate the table by caption ---
# Finds the caption element with the specified text and then finds its parent table element.
# If the caption or table is not found, it prints an error message and exits.
# The caption text is used to identify the correct table in the HTML.
caption = soup.find("caption", string=CAPTION_TEXT)
if not caption:
    print("Could not find caption with schedule table.")
    exit()
table = caption.find_parent("table")
if not table:
    print("Could not find schedule table element.")
    exit()
print("Schedule table found.")



# --- Parse the table rows ---
# Finds all the rows in the table body and iterates through them.
#find_all("tr") finds all the table row elements in the table body.
rows = table.find("tbody").find_all("tr")
inserted = 0



# --- Iterate through the rows and extract data ---
# For each row, it checks if it's a header row (with 'thead' class) and skips it.
# It then extracts the relevant columns (game day, date, time, winner, loser, scores) and processes them.
for row in rows:
    if 'thead' in row.get('class', []):
        continue
    
    # find_all("td") finds all the table data elements in the row.
    # If there are fewer than 10 columns, it skips the row.
    # This is to ensure that the row contains all the necessary data.
    cols = row.find_all("td")
    if len(cols) < 10:
        continue
    
    # Extracting data from the columns
    # text.strip() removes any leading or trailing whitespace from the text.
    # this does not include spaces between words.
    week_raw = row.find("th").text.strip() # The first column is the week number (th representing 'table header')
    game_day = cols[0].text.strip() # The first column of the row (td) is the game day
    game_date_raw = cols[1].text.strip() # The second column of the row (td) is the game date
    game_time_raw = cols[2].text.strip() # The third column of the row (td) is the game time
    winner = cols[3].text.strip() # The fourth column of the row (td) is the winner
    at_symbol = cols[4].text.strip() # The fifth column of the row (td) is the at symbol (@ or vs)
    loser = cols[5].text.strip() # The sixth column of the row (td) is the loser
    winner_score_raw = cols[7].text.strip() # The eighth column of the row (td) is the winner's score
    loser_score_raw = cols[8].text.strip() # The ninth column of the row (td) is the loser's score

    # --- Week Number ---
    # The week number can be either a digit or a special label (like WildCard, Division, etc.)
    # If it's a digit, it converts it to an integer.
    # If it's a special label, it looks it up in the WEEK_LABELS dictionary (From Above)
    if week_raw.isdigit():
        week = int(week_raw)
    else:
        week = WEEK_LABELS.get(week_raw.replace(" ", ""))
        if not week:
            print(f"⚠️ Unknown week label: {week_raw}")
            continue

    # --- Season Type ---
    # The season type is determined based on the week number.
    # If the week number is 18 or higher, it's considered postseason.
    season_type = 'Postseason' if week >= 18 else 'Regular'

    # --- Game Date and Time ---
    # The game date and time are extracted from the raw strings.
    # The date is parsed using strptime to convert it to a date object.
    # The time is parsed using strptime to convert it to a time object.
    try:
        game_date = datetime.strptime(game_date_raw, "%Y-%m-%d").date()
        game_time = datetime.strptime(game_time_raw, "%I:%M%p").time()
    except Exception as e:
        print(f"⚠️ Error parsing datetime: {e}")
        continue
    
    # --- Winner and Loser ---
    # The winner and loser are extracted from the columns.
    # The Winner / Loser is converted to its abbreviation using the TEAM_NAME_TO_ABBR dictionary.
    # Also checks if the abbreviation exists in the dictionary. (Team Exists)
    winner_abbr = TEAM_NAME_TO_ABBR.get(winner)
    loser_abbr = TEAM_NAME_TO_ABBR.get(loser)
    if not winner_abbr or not loser_abbr:
        print(f"Unknown team abbreviation: {winner} / {loser}")
        continue

    # --- TeamID Lookup ---
    # The TeamID is looked up in the database using the abbreviation.
    # It executes a SQL query to fetch the TeamID for the winner and loser.
    # if the TeamID is not found, it prints a warning message and stops the process.
    cursor.execute("SELECT TeamID FROM Team WHERE Abbreviation = %s", (winner_abbr,))
    winner_team_id = cursor.fetchone()
    cursor.execute("SELECT TeamID FROM Team WHERE Abbreviation = %s", (loser_abbr,))
    loser_team_id = cursor.fetchone()
    if not winner_team_id or not loser_team_id:
        print(f"⚠️ Missing TeamIDs for {winner} or {loser}")
        break
    
    # Assigning the TeamIDs to variables
    winner_team_id = winner_team_id[0]
    loser_team_id = loser_team_id[0]
    
    # --- Home and Away Team ---
    # The home and away teams are determined based on the at symbol (@ or vs).
    # If the at symbol is '@', the winner is the home team and the loser is the away team.
    # If there is no at symbol, the winner is the away team and the loser is the home team.
    home_team_id = loser_team_id if at_symbol == '@' else winner_team_id
    away_team_id = winner_team_id if at_symbol == '@' else loser_team_id

    # --- Check for Duplicate Game ---
    # It executes a SQL query to check if the game already exists in the database.
    # If cursor.fetchone() returns a result, it means the game already exists.
    # fetchone() returns the first row of the result set.
    cursor.execute("""
        SELECT GameID FROM Game
        WHERE SeasonID = %s AND GameWeek = %s AND HomeTeamID = %s AND AwayTeamID = %s
    """, (SEASON_ID, week, home_team_id, away_team_id))
    if cursor.fetchone():
        print(f"Duplicate game: Week {week} {winner} vs {loser}")
        break


    # -- Insert into Game --
    # It executes a SQL query to insert the game data into the Game table.
         # SEASONID is Auto-incremented, so we don't need to specify it.
         # Otherwise INSERT INTO lines up with the VALUES lines.
    cursor.execute("""
        INSERT INTO Game (
            SeasonID, GameWeek, GameDay, GameDate, GameTime,
            SeasonType, HomeTeamID, AwayTeamID
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        SEASON_ID, week, game_day, game_date, game_time,
        season_type, home_team_id, away_team_id
    ))
    
    # Gets the Last Inserted ID (GameID) from the Game table
    # This is used to link the Game with its Game Participants.
    game_id = cursor.lastrowid

    # --- Score Parsing ---
    # The winner and loser scores are extracted from the columns.
    # Checks if the scores are valid integers.
    try:
        winner_score = int(winner_score_raw)
        loser_score = int(loser_score_raw)
    except ValueError:
        print(f"Invalid score: {winner_score_raw} or {loser_score_raw}")
        continue

    # --- Insert into GameParticipant ---
    # With the current game_id, it inserts the game participants into the GameParticipant table.
    # The winner is marked as TRUE and the loser as FALSE.
    # Game ID will be the Same for both Participants.
    cursor.execute("""
        INSERT INTO GameParticipant (GameID, TeamID, PointsScored, IsWinner)
        VALUES (%s, %s, %s, TRUE)
    """, (game_id, winner_team_id, winner_score))

    cursor.execute("""
        INSERT INTO GameParticipant (GameID, TeamID, PointsScored, IsWinner)
        VALUES (%s, %s, %s, FALSE)
    """, (game_id, loser_team_id, loser_score))

    inserted += 1 # Increment the inserted count
    print(f"Inserted Week {week} ({season_type}): {winner} vs {loser}")

# --- Commit and Close ---
# Commits the changes to the database and closes the cursor and connection.
# conn.commit() saves the changes to the database.
# cursor.close() closes the cursor.
# conn.close() closes the database connection.
conn.commit()
cursor.close()
conn.close()
print(f"\n🎉 Done! Inserted {inserted} games and GameParticipant rows.")