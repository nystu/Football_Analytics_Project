import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import mysql.connector
import time
import os

# --- MySQL Connect ---
# ===================== 
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



# --- Constants ---
# =================
# The season ID for the current season is set to 2425.
# This ID is used to identify the season in the database.
# The log file name is set to "slug_failures.log".
# This file will be used to log any failures in finding player stats
# For example, if the player page does not exist or the name/birthdate do not match.
season_id = 2425 
LOG_FILE = "slug_failures.log"



# --- Player URLs ---
# ===================
# These are outliers that we need to fetch manually from the Pro Football Reference website.
# The format for these do not follow the standard URL pattern from gameStats.py
player_urls = {
    99:   "https://www.pro-football-reference.com/players/J/JackKa99/gamelog/2024/",  # Kareem Jackson
    127:  "https://www.pro-football-reference.com/players/T/TorrOC00/gamelog/2024/",  # O'Cyrus Torrence
    131:  "https://www.pro-football-reference.com/players/V/VanDRy00/gamelog/2024/",  # Ryan Van Demark
    171:  "https://www.pro-football-reference.com/players/J/JansJ.00/gamelog/2024/",  # J.J Jansen
    189:  "https://www.pro-football-reference.com/players/P/PineEd00/gamelog/2024/",  # Eddy Piñeiro
    262:  "https://www.pro-football-reference.com/players/M/MoorD.00/gamelog/2024/",  # D.J. Moore
    315:  "https://www.pro-football-reference.com/players/H/HillB.00/gamelog/2024/",  # B.J. Hill
    402:  "https://www.pro-football-reference.com/players/M/McGiT.00/gamelog/2024/",  # T.Y. McGill
    482:  "https://www.pro-football-reference.com/players/B/BuntSe00/gamelog/2024/",  # Sean Murphy-Bunting
    489:  "https://www.pro-football-reference.com/players/P/PratMa20/gamelog/2024/",  # Matt Prater
    530:  "https://www.pro-football-reference.com/players/G/GoodC.00/gamelog/2024/",  # C.J. Goodwin
    537:  "https://www.pro-football-reference.com/players/J/JoseLi99/gamelog/2024/",  # Linval Joseph
    599:  "https://www.pro-football-reference.com/players/J/JoneD.01/gamelog/2024/",  # D.J. Jones
    691:  "https://www.pro-football-reference.com/players/R/ReadD.00/gamelog/2024/",  # D.J. Reader
    701:  "https://www.pro-football-reference.com/players/S/StxxAm00/gamelog/2024/",  # Amon-Ra St. Brown
    710:  "https://www.pro-football-reference.com/players/W/WillJo16/gamelog/2024/",  # Jonah Williams
    789:  "https://www.pro-football-reference.com/players/D/DellNa00/gamelog/2024/",  # Tank Dell
    806:  "https://www.pro-football-reference.com/players/H/HughJe99/gamelog/2024/",  # Jerry Hughes
    830:  "https://www.pro-football-reference.com/players/S/StewM.00/gamelog/2024/",  # M.J. Stewart
    940:  "https://www.pro-football-reference.com/players/A/AlleJo03/gamelog/2024/",  # Josh Hines-Allen
    975:  "https://www.pro-football-reference.com/players/V/VanxCo00/gamelog/2024/",  # Cole Van Lanen
    1005: "https://www.pro-football-reference.com/players/H/HumpD.00/gamelog/2024/",  # D.J. Humphries
    1078: "https://www.pro-football-reference.com/players/B/BluxKy00/gamelog/2024/",  # Kyu Blu Kelly
    1129: "https://www.pro-football-reference.com/players/D/DuprAl00/gamelog/2024/",  # Bud Dupree
    1197: "https://www.pro-football-reference.com/players/D/DuraDe01/gamelog/2024/",  # Cobie Durant
    1262: "https://www.pro-football-reference.com/players/C/CampCa99/gamelog/2024/",  # Calais Campbell
    1265: "https://www.pro-football-reference.com/players/A/AndeRo04/gamelog/2024/",  # Robbie Chosen
    1341: "https://www.pro-football-reference.com/players/H/HamxC.00/gamelog/2024/",  # C.J. Ham
    1370: "https://www.pro-football-reference.com/players/R/RodrLe00/gamelog/2024/",  # Levi Drake Rodriguez
    1371: "https://www.pro-football-reference.com/players/R/RomoJo00/gamelog/2024/",  # John Parker Romo
    1471: "https://www.pro-football-reference.com/players/G/GrayJ.00/gamelog/2024/",  # J.T. Gray
    1530: "https://www.pro-football-reference.com/players/B/BashCa00/gamelog/2024/",  # Boogie Basham
    1545: "https://www.pro-football-reference.com/players/G/GanoGr44/gamelog/2024/",  # Graham Gano
    1643: "https://www.pro-football-reference.com/players/M/MoslC.00/gamelog/2024/",  # C.J. Mosley
    1648: "https://www.pro-football-reference.com/players/R/ReedD.00/gamelog/2024/",  # D.J. Reed
    1695: "https://www.pro-football-reference.com/players/G/GardCh00/gamelog/2024/",  # C.J. Gardner-Johnson
    1698: "https://www.pro-football-reference.com/players/G/GrahBr99/gamelog/2024/",  # Brandon Graham
    1731: "https://www.pro-football-reference.com/players/U/UzomC.00/gamelog/2024/",  # C.J. Uzomah
    1759: "https://www.pro-football-reference.com/players/J/JohnBr23/gamelog/2024/",  # Brandon Johnson
    1795: "https://www.pro-football-reference.com/players/W/WattT.00/gamelog/2024/",  # T.J. Watt
    1863: "https://www.pro-football-reference.com/players/W/WillTr21/gamelog/2024/",  # Trent Williams
    1867: "https://www.pro-football-reference.com/players/Y/Ya-SRo00/gamelog/2024/",  # Rock Ya-Sin
    1932: "https://www.pro-football-reference.com/players/W/WoolTa00/gamelog/2024/",  # Riq Woolen
    2022: "https://www.pro-football-reference.com/players/F/FolkNi20/gamelog/2024/",  # Nick Folk
    2069: "https://www.pro-football-reference.com/players/W/WillJa15/gamelog/2024/",  # James Williams
    2086: "https://www.pro-football-reference.com/players/H/HarrDe07/gamelog/2024/",  # Deonte Harty
    2101: "https://www.pro-football-reference.com/players/M/MaduJu00/gamelog/2024/",  # Nnamdi Madubuike
    2108: "https://www.pro-football-reference.com/players/O/OwehJa00/gamelog/2024/",  # Odafe Oweh
    2164: "https://www.pro-football-reference.com/players/M/MartJa04/gamelog/2024/",  # Quan Martin
}


# --- Find PlayerIDs ---
# =====================+
# We already know the players we want to fetch (from the player_urls dictionary).
# So we construct a query to select only those PlayerIDs from the Player table.
player_ids = list(player_urls.keys())  # Get all PlayerIDs from the dictionary
format_strings = ','.join(['%s'] * len(player_ids))  # SQL formatting placeholders
query = f"""
    SELECT PlayerID, FirstName, LastName, BirthDate
        FROM Player
        WHERE PlayerID IN ({format_strings})
        ORDER BY PlayerID ASC
"""
cursor.execute(query, tuple(player_ids))
players = cursor.fetchall()



# --- Rate Limit Handling ---
# ===========================
# To avoid rate limits, we fetch only 18 pages (URLs) per minute.
# After 20 fetches, the script pauses for 60 seconds before continuing.
# Initialize the URL counter and last reset time.
URL_LIMIT = 15
URL_RESET_INTERVAL = 60  # seconds
url_counter = 0
last_reset_time = time.time()



# --- Loop through each player from the database ---
# ==================================================
# For each player, we will try to find their stats on the Pro Football Reference website.
# First we extract the PlayerID, FirstName, LastName, and BirthDate from the player tuple.
# This is done so we can construct the expected URL and check if the stats are available.
for player in players:
    player_id, first_name, last_name, birth_date = player
    expected_name = f"{first_name} {last_name}".lower()
    expected_birth = birth_date.strftime("%Y-%m-%d")
    print(f"\n🎯 Looking for: {expected_name} (Born {expected_birth})")


    # --- Skip players not in URL map ---
    # Should not happen, but just in case.
    if player_id not in player_urls:
        print(f"⏭️ Skipping PlayerID {player_id} — no URL provided.")
        continue
    
    
    # Sets the URL to the value from the player_urls dictionary (Key)
    # debug statement to show the URL being used
    url = player_urls[player_id]
    print(f"🔗 Using direct URL for PlayerID {player_id}: {url}")


    # --- Rate Limit Check ---
    # contunues to update current_time and check if the URL limit has been reached.
    # If the URL limit is reached, it sleeps for the remaining time before continuing.
    current_time = time.time()
    if url_counter >= URL_LIMIT:
        elapsed = current_time - last_reset_time
        if elapsed < URL_RESET_INTERVAL:
            wait_time = URL_RESET_INTERVAL - elapsed
            print(f"⏳ URL limit reached. Sleeping for {int(wait_time)} seconds...")
            time.sleep(wait_time)
        url_counter = 0
        last_reset_time = time.time()

    url_counter += 1
            
    
    # --- Try to load the page ---
    # We use the requests library to fetch the page.
    # If the page loads successfully, we parse it using BeautifulSoup.
    # If it fails, we catch the exception and print a message, then continue to the next slug.
    # (Breaking the loop for this slug if it fails)
    # If the page loads successfully, we parse it using BeautifulSoup.
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9'
        }, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠️ Failed to load gamelog: {e}")
        continue
    soup = BeautifulSoup(response.text, "html.parser")


# --- Player Found Scrape the Stats ---
# =====================================
# If the Player is found, we proceed to scrape the stats from the page.
# We need to be sure to check both the regular season and playoffs stats.
# Assigning a Label to the regular season and playoffs stats.
for table_id in ["stats", "stats_playoffs"]:
    label = "Regular Season" if table_id == "stats" else "Playoffs"
    print(f"\n📊 Checking {label} stats for {expected_name.title()}...")


    # --- Find the table in the HTML ---
    # First we try to find the table directly using the table_id.
    # If not found, we look for it in the comments (for some reason, the table is sometimes commented out).
    # We use BeautifulSoup to parse the HTML and find the table with the specified ID.
    table = soup.find("table", {"id": table_id})
    if not table:
        for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
            if f'id="{table_id}"' in comment:
                table = BeautifulSoup(comment, "html.parser").find("table", {"id": table_id})
                break
    if not table:
        print(f"🚫 {label} table ('{table_id}') not found. Skipping.")
        continue
    print(f"✅ Found '{table_id}' table.")


    # --- Stats Mapping ---
    # We define a mapping of the stats from the table to the database fields.
    # This mapping is used to convert the stats from the table format to the database format.
    STAT_KEYS = {
        
        # Offensive stats
        'pass_att': 'PassingAttempts', 
        'pass_cmp': 'PassingCompletions', 
        'pass_yds': 'PassingYards',
        'pass_td': 'PassingTDs', 
        'pass_int': 'OffensiveInterceptions', 
        'fumbles': 'OffensiveFumbles',
        'rush_att': 'RushingAttempts', 
        'rush_yds': 'RushingYards', 
        'rush_td': 'RushingTDs',
        'rec': 'Receptions', 
        'rec_yds': 'ReceivingYards', 
        'rec_td': 'ReceivingTDs',
        
        # Defensive stats
        'tackles_combined': 'Tackles', 
        'sacks': 'Sacks', 
        'fumbles_forced': 'ForcedFumbles',
        'def_int': 'DefensiveInterceptions', 
        'def_int_yds': 'DefensiveYards', 
        'def_int_td': 'DefensiveTDs',
        
        # Special teams stats
        'fgm': 'FieldGoalsMade',
        'fga': 'FieldGoalsAttempted', 
        'xpm': 'ExtraPointsMade',
        'xpa': 'ExtraPointsAttempted', 
        'punt': 'PuntsAttempted', 
        'punt_yds': 'PuntsYards'
    }



    # --- Populate the GameStats Table ---
    # ====================================
    # --- Loop through all <tr> rows inside the <tbody> of the stats table ---
    # <tbody> is the HTML tag that contains all data rows in a table (excluding the column headers)
    # Each <tr> (table row) inside <tbody> represents a single game played by the player
    # This loop processes each game row and extracts stats for insertion into the database
    rows = table.find("tbody").find_all("tr")


    # --- Enumerate through each table row (<tr>) ---
    # 'idx' is the index (0-based) of the row within the list of all rows
    # 'row' is the BeautifulSoup object representing one <tr> (a single game stat line)
    for idx, row in enumerate(rows):
        
        
        # --- Skip rows that are just internal headers ---
        # Some tables use additional header rows (with class="thead") within <tbody> to separate sections
        if "thead" in row.get("class", []):
            continue


        # --- Skip rows for players who did not participate in the game ---
        # Rows with class="partial_table" are placeholders (e.g., "Did Not Play", "Inactive")
        if "partial_table" in row.get("class", []):
            continue


        # --- Extract the stat data from each <td> (table cell) inside the row ---
        # Each cell contains one stat value and is marked with a "data-stat" attribute (e.g., data-stat="pass_yds")
        # This dictionary comprehension collects all available stats for the row
        row_data = {
            c.get("data-stat"): c.text.strip()  # key = stat name, value = stat value as clean string
            for c in row.find_all("td")         # get all <td> elements
            if c.get("data-stat")               # only include cells with a data-stat attribute
        }


        # --- Extract the game date string ---
        # It should be in the format 'YYYY-MM-DD'; if missing or invalid, skip the row
        # try to convert the string to a date object for the database format year-month-day
        # if conversion fails, skip the row
        date_str = row_data.get("date", "")
        if not date_str or len(date_str) != 10:
            continue
        try:
            game_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            continue


        # --- Get the team abbreviation (e.g., 'BUF', 'KC') from the row ---
        # This is done so we know which team the player played for in this game (TeamID)
        # When then can look up the TeamID with this abbreviation in the Team table
        # But this will only provide us with the whole tuple, so we need to extract the TeamID
        team_abbr = row_data.get("team_name_abbr", "").upper()
        cursor.execute("""
                       SELECT TeamID 
                            FROM Team 
                            WHERE Abbreviation = %s""", (team_abbr,))
        team_row = cursor.fetchone()
        if not team_row:
            print(f"❌ Unknown team: {team_abbr}")
            continue  # Skip if team not found in Team table


        # --- Extract TeamID from the result tuple ---
        # TeamID will always be the first column in the result set (Auto-generated by MySQL)
        team_id = team_row[0]


        # --- Look for the corresponding GameID in the Game table ---
        # Match by date, season ID, and team (either home or away)
        # Date is the game date, SeasonID is the constant and TeamID is EITHER home or away team
        cursor.execute("""
                        SELECT GameID FROM Game
                            WHERE GameDate = %s AND SeasonID = %s
                            AND (HomeTeamID = %s OR AwayTeamID = %s)
        """, (game_date, season_id, team_id, team_id))
        game_row = cursor.fetchone()
        if not game_row:
            print(f"❌ No game match on {game_date} with team {team_abbr}")
            continue

        # --- Extract the GameID from the result ---
        # Same as above for TeamID, GameID is always the first column in the result set
        # We need this to insert the stats into the GameStats table
        game_id = game_row[0]
        

        # --- Define helper to get and convert a stat value safely ---
        # This function retrieves a stat value from the row_data dictionary (above)
        # It removes the percent sign if present and converts it to the appropriate type (INT)
        # If the stat is not found or conversion fails, it returns a default value (0)
        def get_stat(stat, default=0, cast=int):
            raw = row_data.get(stat, '').replace('%', '')  # remove percent sign if present
            if raw == '':
                return default
            try:
                return cast(raw)
            except:
                return default


        # --- Map scraped stats to database fields ---
        # We use the STAT_KEYS dictionary to map the scraped stats to the database fields
        # The db_feild is the name of the field in the database (e.g., PassingAttempts)
        stats = {
            db_field: get_stat(stat, cast=float if db_field == 'Sacks' else int)
            for stat, db_field in STAT_KEYS.items()
        }


        # --- Prepare fields for SQL INSERT ---
        # GameID is the Primary key and PlayerID and TeamID are Foreign keys
        # The List of the stat keys are in the order they are in the database
        insert_fields = ['GameID', 'PlayerID', 'TeamID'] + list(stats.keys())

        # --- Generate placeholders for parameterized query (e.g., '%s, %s, %s, ...') ---
        # For now we create a string with the same number of placeholders as there are fields
        # This is done so we can use a parameterized query to prevent SQL injection
        placeholders = ', '.join(['%s'] * len(insert_fields))


        # --- Create ON DUPLICATE KEY UPDATE clause ---
        # If a record already exists for this (GameID, PlayerID, TeamID), update the stats instead of inserting a duplicate
        # This is so we can update the stats for a player if they have already played in this game (or need to update a specific stat)
        # More or less to make sure we don't have duplicates in the database
        update_clause = ', '.join([
            f"{f}=VALUES({f})"
            for f in insert_fields if f not in ('GameID', 'PlayerID', 'TeamID')
        ])


        # --- Prepare the SQL query ---
        # =============================
        # insert felds are the columns to insert into in the database
        # placeholders are the values to insert (e.g., '%s, %s, %s, ...')
        # The ON DUPLICATE KEY UPDATE clause specifies what to do if a duplicate key is found
        sql = f"""
            INSERT INTO GameStats ({', '.join(insert_fields)})
                VALUES ({placeholders})
                ON DUPLICATE KEY UPDATE {update_clause}
        """
        values = [game_id, player_id, team_id] + list(stats.values())


        # --- Execute the query and commit the changes ---
        # Puts the values into the placeholders in the SQL query
        # Then commits the changes to the database
        cursor.execute(sql, values)
        conn.commit()

        # --- Print confirmation for this row ---
        # THis is done for debugging purposes to see which rows are being inserted
        # Or which rows are being skipped since the player was inactive or did not play (Above)
        print(f"✅ Inserted {label} stats for {game_date} (Team: {team_abbr})")

# --- Done ---
# After processing all players, we close the database connection.
# We commit the changes to the database and close the cursor and connection.
cursor.close()
conn.close()
print("\n🧹 Done with players.")

# --- Print Log File Contents (Optional Summary) ---
if os.path.exists(LOG_FILE):
    print(f"\n📄 Contents of {LOG_FILE}:")
    with open(LOG_FILE, "r") as log:
        print(log.read().strip())
else:
    print("\n✅ No failed player matches logged.")
    