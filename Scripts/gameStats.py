import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import mysql.connector
import time
import os
import re

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



# --- Execute SQL Query For All Players ---
# =========================================
# This SQL query selects the PlayerID, FirstName, LastName, and BirthDate from the Player table.
# The results are ordered by PlayerID in ascending order.
cursor.execute("""
               SELECT PlayerID, FirstName, LastName, BirthDate 
                    FROM Player 
                    ORDER BY PlayerID ASC
                """)
players = cursor.fetchall()


# --- Rate Limit Handling ---
# ===========================
# To avoid rate limits, we fetch only 18 pages (URLs) per minute.
# After 20 fetches, the script pauses for 60 seconds before continuing.
# Initialize the URL counter and last reset time.
URL_LIMIT = 18
URL_RESET_INTERVAL = 60  # seconds
url_counter = 0
last_reset_time = time.time()



# --- Helper: Normalize Names for Slug Construction ---
# =====================================================
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
    # Combine and format
    ln_padded = ln[:4].ljust(4, 'x')
    return (ln_padded + fn[:2]).title()



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
    # This is because the prefix is not always unique, so we need to try different combinations.
    # contunues to update current_time and check if the URL limit has been reached.
    # If the URL limit is reached, it sleeps for the remaining time before continuing.
    for i in range(8):
        current_time = time.time()
        if url_counter >= URL_LIMIT:
            elapsed = current_time - last_reset_time
            if elapsed < URL_RESET_INTERVAL:
                wait_time = URL_RESET_INTERVAL - elapsed
                print(f"⏳ URL limit reached. Sleeping for {int(wait_time)} seconds...")
                time.sleep(wait_time)
            url_counter = 0 # reset the counter after sleeping
            last_reset_time = time.time() # update the last reset time
        
        
        # --- Construct the slug and URL ---
        # The slug is constructed by taking the slug_prefix and appending a two-digit suffix.
        # From this it creates the URL for the player's gamelog page.
        # Increasing the URL Counter each time to make sure we don't exceed the limit.
        suffix = f"{i:02d}"
        slug = f"{slug_prefix}{suffix}"
        url = f"https://www.pro-football-reference.com/players/{slug_letter}/{slug}/gamelog/2024/"
        print(f"🔍 Trying slug: {slug} → {url}")
        url_counter += 1  # ✅ Count all fetches regardless of success


        # --- Try to load the page ---
        # We use the requests library to fetch the page.
        # If the page loads successfully, we parse it using BeautifulSoup.
        # If it fails, we catch the exception and print a message, then continue to the next slug.
        # (Breaking the loop for this slug if it fails)
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept-Language': 'en-US,en;q=0.9'
            }, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"⚠️ Failed to load gamelog: {e}")
            continue


        # --- Check Page and Player Match ---
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


        # --- Extract Name and Birthdate ---
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



    # --- Log Failure ---
    # ===================
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




# --- Close Cursor and Connection ---
# ===================================
# After processing all players, we close the database connection.
# We commit the changes to the database and close the cursor and connection.
cursor.close()
conn.close()
print("\n🧹 Done with players.")

    
