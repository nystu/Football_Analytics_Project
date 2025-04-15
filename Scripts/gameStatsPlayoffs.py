import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import mysql.connector
import time
import os
import re

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
# These ae used to track the players that could not find stats for on the website.
season_id = 2425 
LOG_FILE = "slug_failures.log"

# --- Execute SQL Query ---
# This SQL query selects the PlayerID, FirstName, LastName, and BirthDate from the Player table.
# The results are ordered by PlayerID in ascending order.
cursor.execute("SELECT PlayerID, FirstName, LastName, BirthDate FROM Player ORDER BY PlayerID ASC")
players = cursor.fetchall()

# --- Rate Limit Handling ---
# To avoid rate limits, we fetch only 20 pages (URLs) per minute.
# After 20 fetches, the script pauses for 60 seconds before continuing.
URL_LIMIT = 15
URL_RESET_INTERVAL = 60  # seconds
url_counter = 0
last_reset_time = time.time()

# --- Helper: Normalize Names for Slug Construction ---
# Handles edge cases in names like apostrophes, periods, compound names, and short last names.
def normalize_slug_prefix(last_name, first_name):
    import re

    # Remove non-alphabetic characters from each name part
    ln = re.sub(r"[^a-zA-Z]", "", last_name)
    fn = re.sub(r"[^a-zA-Z]", "", first_name)

    # Handle compound last names like "Van Demark"
    if " " in last_name:
        parts = last_name.split(" ")
        if len(parts) > 1:
            ln = parts[0].capitalize() + parts[1][0:2].capitalize()
    elif "'" in last_name or "." in last_name:
        ln = re.sub(r"[^a-zA-Z]", "", last_name)

    # Pad short last names with 'x' if fewer than 4 characters
    ln_padded = ln[:4].ljust(4, 'x')

    # Combine and format
    return (ln_padded + fn[:2]).title()

# --- Loop through each player ---
# For each player, we will try to find their stats on the Pro Football Reference website.
# First we extract the PlayerID, FirstName, LastName, and BirthDate from the player tuple.
# This is done so we can construct the expected URL and check if the stats are available.
for player in players:
    player_id, first_name, last_name, birth_date = player
    expected_name = f"{first_name} {last_name}".lower()
    expected_birth = birth_date.strftime("%Y-%m-%d")
    print(f"\n🎯 Looking for: {expected_name} (Born {expected_birth})")

    # --- Construct Slug (URL) ---
    # The slug_letter is the first letter of the last name, converted to uppercase.
    # The slug_prefix is constructed by taking the first four letters of the last name
    # and the first two letters of the first name, and converting them to title case.
    # Found is initialized to False, indicating that we haven't found the player yet.
    slug_letter = last_name[0].upper()
    slug_prefix = normalize_slug_prefix(last_name, first_name)
    found = False

    # --- Try Slugs ---
    # This loop tries to construct the URL for the player's gamelog page.
    # It appends a two-digit suffix (00 to 04) to the slug_prefix and constructs the URL.
    # This is because the prefix is not always unique, so we need to try different combinations.
    for i in range(5):
        # --- Rate Limit Check Based on URL Fetches ---
        current_time = time.time()
        if url_counter >= URL_LIMIT:
            elapsed = current_time - last_reset_time
            if elapsed < URL_RESET_INTERVAL:
                wait_time = URL_RESET_INTERVAL - elapsed
                print(f"⏳ URL limit reached. Sleeping for {int(wait_time)} seconds...")
                time.sleep(wait_time)
            url_counter = 0
            last_reset_time = time.time()

        suffix = f"{i:02d}"
        slug = f"{slug_prefix}{suffix}"
        url = f"https://www.pro-football-reference.com/players/{slug_letter}/{slug}/gamelog/2024/"

        # --- Fetch the page ---
        # This part fetches the page using requests and BeautifulSoup.
        # It sets a user-agent and accept-language header to mimic a real browser.
        # It also handles exceptions if the page fails to load.
        # If the page fails to load, it indicates that the URL is not valid or the player does not exist.
        print(f"🔍 Trying slug: {slug} → {url}")
        url_counter += 1  # ✅ Always count the request attempt

        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept-Language': 'en-US,en;q=0.9'
            }, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"⚠️ Failed to load gamelog: {e}")
            continue


        # --- Parse the page ---
        # If the page loads successfully, we parse it using BeautifulSoup.
        # But first we need to identify if it the player that we are looking for.
        # We look for the player's name and birthdate in the HTML.
        soup = BeautifulSoup(response.text, "html.parser")
        name_tag = soup.select_one("h1 span")
        birth_tag = soup.select_one("#necro-birth[data-birth]")

        if not birth_tag:
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                comment_soup = BeautifulSoup(comment, "html.parser")
                birth_tag = comment_soup.select_one("#necro-birth[data-birth]")
                if birth_tag:
                    break

        if not name_tag or not birth_tag:
            print("❌ Name or birthdate not found.")
            continue

        # Extract the player's name and birthdate from the HTML.
        # The name is extracted from the <h1> tag and the birthdate from the <span> tag with id "necro-birth".
        page_name = name_tag.text.strip().lower()
        page_birth = birth_tag.get("data-birth", "").strip()

        # --- Check for match ---
        # We check if the extracted name and birthdate match the expected values.
        # If they match, we set found to True and break out of the inner loop.
        # Then we proceed to locate the stats table.
        # If they do not match, we print a message indicating the mismatch.
        if page_name == expected_name and page_birth == expected_birth:
            print(f"✅ Match found: {page_name.title()} ({page_birth})")
            found = True
            break
        else:
            print(f"❌ Mismatch: Got {page_name.title()} ({page_birth})")
            time.sleep(1)



    # --- Check if found ---
    # If found is still False after trying all slugs, we log the failure.
    # We create a log line with the player's ID, name, birthdate, and the slugs that were tried.
    # We also write this log line to the log file.
    # At the end, we print a message indicating that the player was not found.
    if not found:
        print("🚫 Could not find matching player.")
        failed_slugs = [f"{slug_prefix}{i:02d}" for i in range(5)]
        log_line = (
            f"{datetime.now().isoformat()} | PlayerID: {player_id} | Name: {first_name} {last_name} "
            f"(Born {birth_date}) | Tried slugs: {', '.join(failed_slugs)}\n"
        )
        try:
            with open(LOG_FILE, "a") as log:
                log.write(log_line)
            print(f"📝 Logged failed attempt to {LOG_FILE}")
        except Exception as log_err:
            print(f"⚠️ Could not write to log file: {log_err}")
        continue



    # --- Locate Playoff Stats Table ---
    # ✅ CHANGED: Specifically looks for the playoff stats table (`stats_playoffs`).
    table = soup.find("table", {"id": "stats_playoffs"})
    if not table:
        for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
            if 'id="stats_playoffs"' in comment:
                table = BeautifulSoup(comment, "html.parser").find("table", {"id": "stats_playoffs"})
                break

    if not table:
        print("🚫 Playoff stats table ('stats_playoffs') not found for this player. Moving on...")
        continue

    print("✅ Found 'stats_playoffs' table.")



    # --- Stats Mapping ---
    # This dictionary maps the stats from the website to the database fields.
    # The keys are the stats as they appear on the website, and the values are the corresponding database fields.
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

    
    
    # Finds all the rows in the table body (tbody)
    # Each row represents a game played by the player.
    # the "thread" class is used to identify the header row, which we skip.
    # The "partial_table" class is used to identify rows that are marked as "Did Not Play".
    rows = table.find("tbody").find_all("tr")
    for idx, row in enumerate(rows):
        if "thead" in row.get("class", []):
            continue
        if "partial_table" in row.get("class", []):
            date_str = row.find("td", {"data-stat": "date"})
            date_display = date_str.text if date_str else f"row {idx}"
            print(f"⏭️ Skipping {date_display}: row marked as 'partial_table' (Did Not Play)")
            continue
        
        # --- Extract Player Stats ---
        # Each row contains the player's stats for a specific game.
        # We extract the data from the table cells (td) using the find_all method.
        cells = row.find_all("td")
        if not cells:
            continue
        
        # The data-stat attribute is used to identify the specific stat. (Located in the <td> tag)
        # The first stat we extract is the date of the game. (To match the game with the database)
        row_data = {c.get("data-stat"): c.text.strip() for c in cells if c.get("data-stat")}
        date_str = row_data.get("date", "")
        if not date_str or len(date_str) != 10:
            continue
        
        # Format the date string to match the database format (YYYY-MM-DD)
        # We use the strptime method to parse the date string into a datetime object. 
        # Then we convert it to a date object.
        try:
            game_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            continue

        # --- Check if game date is valid ---
        # We now need the TeamID from the database to check if the game exists.
        team_abbr = row_data.get("team_name_abbr", "").upper()
        cursor.execute("SELECT TeamID FROM Team WHERE Abbreviation = %s", (team_abbr,))
        team_row = cursor.fetchone()
        if not team_row:
            print(f"❌ Unknown team: {team_abbr}")
            print("🛑 Stopping execution due to unmatched team.")
            exit()
        team_id = team_row[0]

        # With the teamID and the game date, we can check if the game exists in the database.
        # We do this by querying the Game table for a matching game date and team ID.
        # Where the HomeTeamID or AwayTeamID matches the team ID.
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

        # We Now can extract the player's stats from the row.
        # We use a helper function to get the stat value from the row data.
        # The function takes the stat name, a default value, and a cast function.
        # The default value is used if the stat is not found or is empty.
        def get_stat(stat, default=0, cast=int):
            raw = row_data.get(stat, '').replace('%', '')
            if raw == '':
                return default
            try:
                return cast(raw)
            except:
                return default

        # With the dictionary comprehension, we create a new dictionary called stats.
        # This dictionary contains the stats for the player in the current game.
        # We use the STAT_KEYS dictionary to map the stats from the website to the database fields.
        # The get_stat function is used to extract the value for each stat.
        # The cast function is used to convert the value to the appropriate type.
        stats = {
            db_field: get_stat(stat, cast=float if db_field == 'Sacks' else int)
            for stat, db_field in STAT_KEYS.items()
        }

        # --- Insert or Update Game Stats ---
        # The Insert Felds are the columns in the GameStats table.
        # We create a list of fields to insert into the database.
        # the placeholders are used to insert the stats as a comma-separated string.
        # The update clause is used to update the stats if the game already exists. (I.E if the player has already played in that game)
        insert_fields = ['GameID', 'PlayerID', 'TeamID'] + list(stats.keys())
        placeholders = ', '.join(['%s'] * len(insert_fields))
        update_clause = ', '.join([f"{f}=VALUES({f})" for f in insert_fields if f not in ('GameID', 'PlayerID', 'TeamID')])
        
        # The SQL query uses the INSERT INTO statement to insert the stats into the GameStats table.
        # We set up what the cursor should execute by using the SQL query and the values.
        # The ON DUPLICATE KEY UPDATE clause is used to update the stats if the game already exists.
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
# At the end of the script, print out all failed player match attempts
# This makes it easy to verify which players could not be found during the run
if os.path.exists(LOG_FILE):
    print(f"\n📄 Contents of {LOG_FILE}:")
    with open(LOG_FILE, "r") as log:
        print(log.read().strip())
else:
    print("\n✅ No failed player matches logged.")