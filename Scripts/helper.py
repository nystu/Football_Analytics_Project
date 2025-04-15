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
    35: "https://www.pro-football-reference.com/players/K/KooxYo00/gamelog/2024/",    # Name: Younghoe Koo
    57: "https://www.pro-football-reference.com/players/S/SmitJa08/gamelog/2024/",    # Name: James Smith-Williams
    91: "https://www.pro-football-reference.com/players/E/EpenAJ00/gamelog/2024/",   # Name: A.J. Epenesa
    99: "https://www.pro-football-reference.com/players/J/JackKa99/gamelog/2024/",    # Name: Kareem Jackson
    127: "https://www.pro-football-reference.com/players/T/TorrOC00/gamelog/2024/",  # Name: O'Cyrus Torrence
    131: "https://www.pro-football-reference.com/players/V/VanDRy00/gamelog/2024/",   # Name: Ryan Van Demark
    189: "https://www.pro-football-reference.com/players/P/PineEd00/gamelog/2024/"   # Name: Eddy Piñeiro
    # 191:    # Name: LaBryan Ray
    # 196:    # Name: A'Shawn Robinson
    # 202:    # Name: T.J. Smith
    # 216:    # Name: D.J. Wonnum
    # 241:    # Name: T.J. Edwards
    # 253:    # Name: Jaylon Johnson
    # 254:    # Name: Roschon Johnson
    # 255:    # Name: Braxton Jones
    # 256:    # Name: Carl Jones
    # 257:    # Name: Jaylon Jones
    # 262:    # Name: D.J. Moore
    # 276:    # Name: Terell Smith
    # 286:    # Name: Chris Williams
    # 289:    # Name: Erick All
    # 295:    # Name: Chase Brown
    # 298:    # Name: Jake Browning
    # 305:    # Name: Jalen Davis
    # 310:    # Name: Lawrence Guy
    # 315:    # Name: B.J. Hill
    # 327:    # Name: Charlie Jones
    # 330:    # Name: Matt Lee
    # 352:    # Name: Trayveon Williams
    # 362:    # Name: Corey Bojorquez
    # 363:    # Name: Jowon Briggs
    # 399:    # Name: Dawand Jones
    # 402:    # Name: T.Y. McGill
    # 464:    # Name: Blake Gillikin
    # 466:    # Name: Marvin Harrison Jr.
    # 471:    # Name: Christian Jones
    # 482:    # Name: Sean Murphy-Bunting
    # 489:    # Name: Matt Prater
    # 505:    # Name: Jonah Williams
    # 530:    # Name: C.J. Goodwin
    # 533:    # Name: Darius Harris
    # 537:    # Name: Linval Joseph
    # 561:    # Name: Mazi Smith
    # 597:    # Name: Jordan Jackson
    # 598:    # Name: Brandon Jones
    # 599:    # Name: D.J. Jones
    # 621:    # Name: Keidron Smith
    # 637:    # Name: Javonte Williams
    # 664:    # Name: Jamarco Jones
    # 691:    # Name: D.J. Reader
    # 699:    # Name: Chris Smith
    # 701:    # Name: Amon-Ra St. Brown
    # 709:    # Name: Jameson Williams
    # 710:    # Name: Jonah Williams
    # 770:    # Name: Malik Willis
    # 789:    # Name: Tank Dell
    # 799:    # Name: Christian Harris
    # 806:    # Name: Jerry Hughes
    # 830:    # Name: M.J. Stewart
    # 876:    # Name: Jaylon Jones
    # 903:    # Name: Braden Smith
    # 908:    # Name: Rodney Thomas II
    # 940:    # Name: Josh Hines-Allen
    # 944:    # Name: Antonio Johnson
    # 947:    # Name: Jarrian Jones
    # 948:    # Name: Mac Jones
    # 970:    # Name: Maason Smith
    # 972:    # Name: Brian Thomas
    # 973:    # Name: Daniel Thomas
    # 975:    # Name: Cole Van Lanen
    # 1005:   # Name: D.J. Humphries
    # 1010:   # Name: Chris Jones
    # 1031:   # Name: Trey Smith
    # 1077:   # Name: Jack Jones
    # 1078:   # Name: Kyu Blu Kelly
    # 1103:   # Name: John Samuel Shenker
    # 1129:   # Name: Bud Dupree
    # 1152:   # Name: Jaylen Johnson
    # 1185:   # Name: Kendall Williamson
    # 1194:   # Name: Tyler Davis
    # 1197:   # Name: Cobie Durant
    # 1211:   # Name: Desjuan Johnson
    # 1212:   # Name: John Johnson
    # 1244:   # Name: Darious Williams
    # 1262:   # Name: Calais Campbell
    # 1265:   # Name: Robbie Chosen
    # 1333:   # Name: Jamin Davis
    # 1341:   # Name: C.J. Ham
    # 1370:   # Name: Levi Drake Rodriguez
    # 1371:   # Name: John Parker Romo
    # 1419:   # Name: Marcus Jones
    # 1471:   # Name: J.T. Gray
    # 1523:   # Name: Jamaal Williams
    # 1530:   # Name: Boogie Basham
    # 1545:   # Name: Graham Gano
    # 1556:   # Name: Anthony Johnson
    # 1558:   # Name: Jakob Johnson
    # 1561:   # Name: Daniel Jones
    # 1604:   # Name: Dee Williams
    # 1606:   # Name: Braelon Allen
    # 1629:   # Name: Jermaine Johnson II
    # 1643:   # Name: C.J. Mosley
    # 1648:   # Name: D.J. Reed
    # 1655:   # Name: Brandon Smith
    # 1667:   # Name: Mike Williams
    # 1683:   # Name: Jalen Carter
    # 1695:   # Name: C.J. Gardner-Johnson
    # 1698:   # Name: Brandon Graham
    # 1725:   # Name: DeVonta Smith
    # 1731:   # Name: C.J. Uzomah
    # 1733:   # Name: Milton Williams
    # 1745:   # Name: Jalen Elliott
    # 1759:   # Name: Brandon Johnson
    # 1761:   # Name: Broderick Jones
    # 1773:   # Name: Dan Moore
    # 1795:   # Name: T.J. Watt
    # 1796:   # Name: Rodney Williams
    # 1862:   # Name: DaShaun White
    # 1863:   # Name: Trent Williams
    # 1864:   # Name: Brayden Willis
    # 1867:   # Name: Rock Ya-Sin
    # 1921:   # Name: Jaxon Smith-Njigba
    # 1928:   # Name: Cody White
    # 1932:   # Name: Riq Woolen
    # 1942:   # Name: Jack Browning
    # 1991:   # Name: Tykee Smith
    # 2012:   # Name: Jarvis Brownlee
    # 2022:   # Name: Nick Folk
    # 2029:   # Name: Jaylen Harrell
    # 2069:   # Name: James Williams
    # 2085:   # Name: Malik Harrison
    # 2086:   # Name: Deonte Harty
    # 2092:   # Name: Josh Johnson
    # 2093:   # Name: Josh Jones
    # 2101:   # Name: Nnamdi Madubuike
    # 2108:   # Name: Odafe Oweh
    # 2114:   # Name: Roquan Smith
    # 2129:   # Name: Marcus Williams
    # 2164:   # Name: Quan Martin
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

    # --- Fetch the page ---
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9'
        }, timeout=10)
        response.raise_for_status()
        url_counter += 1
    except Exception as e:
        print(f"⚠️ Failed to load gamelog: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # --- Locate Playoff Stats Table ---
    # We're looking for the 'stats_playoffs' table instead of the regular season 'stats' table.
    table = soup.find("table", {"id": "stats_playoffs"})
    if not table:
        for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
            if 'id="stats_playoffs"' in comment:
                table = BeautifulSoup(comment, "html.parser").find("table", {"id": "stats_playoffs"})
                break

    if not table:
        print("❌ No playoff stats table found. Skipping player.")
        continue
    print("✅ Found 'stats_playoffs' table.")

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