import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import mysql.connector
import time
import os

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

# Set the season ID for the 2024 Season
# LOG_FILE is the name of the log file where failed attempts will be recorded.
# These are used to track the players that could not find stats for on the website.
season_id = 2425 
LOG_FILE = "slug_failures.log"

player_urls = {
    99:   "https://www.pro-football-reference.com/players/J/JackKa99/gamelog/2024/",  # Kareem Jackson
    127:  "https://www.pro-football-reference.com/players/T/TorrOC00/gamelog/2024/",  # O'Cyrus Torrence
    131:  "https://www.pro-football-reference.com/players/V/VanDRy00/gamelog/2024/",  # Ryan Van Demark
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

# --- Execute SQL Query ---
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
# To avoid rate limits, we fetch only 15 pages (URLs) per minute.
# After 15 fetches, the script pauses for 60 seconds before continuing.
URL_LIMIT = 15
URL_RESET_INTERVAL = 60  # seconds
url_counter = 0
last_reset_time = time.time()

# --- Loop through each player ---
# For each player, we will try to find their stats on the Pro Football Reference website.
# We skip players not included in the manual URL list.
for player in players:
    player_id, first_name, last_name, birth_date = player
    expected_name = f"{first_name} {last_name}".lower()
    expected_birth = birth_date.strftime("%Y-%m-%d")
    print(f"\n🎯 Looking for: {expected_name} (Born {expected_birth})")

    # --- Skip players not in URL map ---
    if player_id not in player_urls:
        print(f"⏭️ Skipping PlayerID {player_id} — no URL provided.")
        continue

    url = player_urls[player_id]
    print(f"🔗 Using direct URL for PlayerID {player_id}: {url}")

    # --- Rate Limit Check ---
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
            
    # --- Fetch the page ---
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

    # --- Locate Regular Season Stats Table ---
    # We're looking for the 'stats' table (regular season), not 'stats_playoffs'
    table = soup.find("table", {"id": "stats"})
    if not table:
        for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
            if 'id="stats"' in comment:
                table = BeautifulSoup(comment, "html.parser").find("table", {"id": "stats"})
                break

    if not table:
        print("❌ No regular season stats table found. Skipping player.")
        continue
    print("✅ Found 'stats' table.")

    # --- Stats Mapping ---
    STAT_KEYS = {
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
        'tackles_combined': 'Tackles',
        'sacks': 'Sacks',
        'fumbles_forced': 'ForcedFumbles',
        'def_int': 'DefensiveInterceptions',
        'def_int_yds': 'DefensiveYards',
        'def_int_td': 'DefensiveTDs',
        'fgm': 'FieldGoalsMade',
        'fga': 'FieldGoalsAttempted',
        'xpm': 'ExtraPointsMade',
        'xpa': 'ExtraPointsAttempted',
        'punt': 'PuntsAttempted',
        'punt_yds': 'PuntsYards'
    }

    rows = table.find("tbody").find_all("tr")
    for idx, row in enumerate(rows):
        if "thead" in row.get("class", []):
            continue
        if "partial_table" in row.get("class", []):
            date_str = row.find("td", {"data-stat": "date"})
            date_display = date_str.text if date_str else f"row {idx}"
            print(f"⏭️ Skipping {date_display}: row marked as 'partial_table' (Did Not Play)")
            continue

        cells = row.find_all("td")
        if not cells:
            continue

        row_data = {c.get("data-stat"): c.text.strip() for c in cells if c.get("data-stat")}
        date_str = row_data.get("date", "")
        if not date_str or len(date_str) != 10:
            continue

        try:
            game_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            continue

        team_abbr = row_data.get("team_name_abbr", "").upper()
        cursor.execute("SELECT TeamID FROM Team WHERE Abbreviation = %s", (team_abbr,))
        team_row = cursor.fetchone()
        if not team_row:
            print(f"❌ Unknown team: {team_abbr}")
            print("🛑 Stopping execution due to unmatched team.")
            exit()
        team_id = team_row[0]

        cursor.execute("""
            SELECT GameID FROM Game
            WHERE GameDate = %s AND SeasonID = %s
            AND (HomeTeamID = %s OR AwayTeamID = %s)
        """, (game_date, season_id, team_id, team_id))
        game_row = cursor.fetchone()
        if not game_row:
            print(f"❌ No game match on {game_date} with team {team_abbr}")
            print("🛑 Stopping execution due to unmatched game.")
            exit()
        game_id = game_row[0]

        def get_stat(stat, default=0, cast=int):
            raw = row_data.get(stat, '').replace('%', '')
            if raw == '':
                return default
            try:
                return cast(raw)
            except:
                return default

        stats = {
            db_field: get_stat(stat, cast=float if db_field == 'Sacks' else int)
            for stat, db_field in STAT_KEYS.items()
        }

        insert_fields = ['GameID', 'PlayerID', 'TeamID'] + list(stats.keys())
        placeholders = ', '.join(['%s'] * len(insert_fields))
        update_clause = ', '.join([f"{f}=VALUES({f})" for f in insert_fields if f not in ('GameID', 'PlayerID', 'TeamID')])

        sql = f"""
            INSERT INTO GameStats ({', '.join(insert_fields)})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {update_clause}
        """
        values = [game_id, player_id, team_id] + list(stats.values())
        cursor.execute(sql, values)
        conn.commit()
        print(f"✅ Inserted stats for {game_date} (Team: {team_abbr})")

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
    
    
# Remove these Players from database
# LaBryan Ray
# John Samuel Shenker