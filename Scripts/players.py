import requests # Fetches HTML from the web
from bs4 import BeautifulSoup, Comment # Parses the HTML content and allows us to navigate and search through it
import mysql.connector # Connects to MySQL database
from datetime import datetime # Handles date and time formatting



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


# --- Scrape Roster ---
# List of NFL team abbreviations
# This list contains the abbreviations for all NFL teams.
# Used to construct the URLs for scraping player data.
team_abbrs = [
    "atl", "buf", "car", "chi", "cin", "cle", "crd", "dal", "den", "det",
    "gnb", "htx", "clt", "jax", "kan", "rai", "sdg", "ram", "mia", "min",
    "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "rav", "was"
]
inserted_total = 0


# Loop through each team abbreviation
# For each team abbreviation, construct the URL for the team's roster page
# Scrapes the roster data from the page
# requests.get() fetches the HTML content from the specified URL.
# BeautifulSoup parses the HTML content, allowing us to search and navigate through it.
for abbr in team_abbrs:
    print(f"Scraping roster for team: {abbr.upper()}")
    url = f"https://www.pro-football-reference.com/teams/{abbr}/2024_roster.htm"
    html = requests.get(url).text 
    soup = BeautifulSoup(html, "html.parser") 

    # --- Find the roster table ---
    # The roster table is embedded in a comment in the HTML.
    # So we need to find the comment that contains the table.
    # To do this, we use BeautifulSoup to search for comments in the HTML.
    # The lambda function checks if the text is a comment, If it is, we check if it contains 'id="roster"'
    table = None
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if 'id="roster"' in comment:
            comment_soup = BeautifulSoup(comment, "html.parser")
            table = comment_soup.find("table", {"id": "roster"})
            break
    if not table:
        print("ERROR: Could not find the roster table.")
        continue

    # --- Parse the table rows ---
    # Find all the rows in the table body (tbody)
    # Each row represents a player 
    # The find_all method returns a list of all matching elements.
    rows = table.tbody.find_all("tr")
    print(f"Found {len(rows)} player rows.")

    # --- Insert players into the database ---
    # Loop through each row and extract player data
    # For each row, we extract the player's name, college, and birth date.
    inserted = 0
    for row in rows:
        
        # Uses try-except to handle any errors that may occur during the extraction process.
        # This is important because the data may not always be in the expected format.
        # Otherwise find_all columns in the row ("td" refers to table data cells)
        try:
            cols = row.find_all("td")
            if len(cols) < 9:
                continue
            
            # We do not care about the column headers, so we skip the first column
            # Then Checks to make sure that the player has a name, college, and birth date
            # If any of these values are missing, we skip the row
            name = cols[0].text.strip() # First column contains the player's name
            college_raw = cols[7].text.strip() # Seventh column contains the college
            birth_raw = cols[8].text.strip() # Eighth column contains the birth date
            if not name or not college_raw or not birth_raw:
                continue
            
            # --- Extract Player Data ---
            # The player's name is in the format "First Last"
            # Need to split the name into first and last names
            # The split() method splits the string into a list of words
            # The first word is the first name, and the rest is the last name
            # Sometimes More than One college is listed, so we take the last one (Most recent)
            # This Insures that the SQL is in 3rd Normal Form (Not storing multiple values in a single column)
            parts = name.split()
            first_name = parts[0]
            last_name = " ".join(parts[1:])
            college = college_raw.split(",")[-1].strip()
            dob = datetime.strptime(birth_raw, "%m/%d/%Y").strftime("%Y-%m-%d")

            # --- Check for duplicates ---
            # Check if the player already exists in the database
            # We do this by querying the Player table for a matching name and birth date (Assuming Name and DOB are unique)
            # If PlayerID is found, we skip the insertion (continue to the next row)
            cursor.execute("""
                SELECT PlayerID FROM Player
                WHERE FirstName = %s AND LastName = %s AND BirthDate = %s
            """, (first_name, last_name, dob))
            if cursor.fetchone():
                print(f"SKIPPING duplicate: {first_name} {last_name}, DOB {dob}")
                continue

            # --- Insert Player Into Database ---
            # If the player does not exist, we insert them into the database
            # Need to Line up INSERT INTO with the correct VALUES
            print(f"✅ Inserting: {first_name} {last_name}, DOB {dob}, College {college}")
            cursor.execute("""
                INSERT INTO Player (FirstName, LastName, BirthDate, College)
                VALUES (%s, %s, %s, %s)
            """, (first_name, last_name, dob, college))
            print(f"✅ Inserted: {first_name} {last_name}, DOB {dob}, College {college}")
            inserted += 1 # Increment the inserted count
            
        except Exception as e:
            print(f"Error inserting player: {e}")

    inserted_total += inserted # Total inserted players
    print(f"INSERTED {inserted} players from {abbr.upper()}") # Player and Team



# --- Commit and Close ---
# Commits the changes to the database and closes the cursor and connection.
# conn.commit() saves the changes to the database.
# cursor.close() closes the cursor.
# conn.close() closes the database connection.
conn.commit()
cursor.close()
conn.close()
print(f"\nFINISHED! Inserted {inserted} games and GameParticipant rows.")