import requests
from bs4 import BeautifulSoup, Comment
import mysql.connector
from datetime import datetime

# Connect to MySQL
conn = mysql.connector.connect(
    host="138.49.184.47",
    port=3306,
    user="nystuen6918",
    password="MdSDU6V2!g3aNZxb",
    database="nystuen6918_FA_Project"
)
cursor = conn.cursor()

# Alphabetical team abbreviations
team_abbrs = [
    "atl", "buf", "car", "chi", "cin", "cle", "crd", "dal", "den", "det",
    "gnb", "htx", "clt", "jax", "kan", "rai", "sdg", "ram", "mia", "min",
    "nwe", "nor", "nyg", "nyj", "phi", "pit", "sfo", "sea", "tam", "oti", "rav", "was"
]

inserted_total = 0

for abbr in team_abbrs:
    print(f"\n📄 Scraping roster for team: {abbr.upper()}")

    url = f"https://www.pro-football-reference.com/teams/{abbr}/2024_roster.htm"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # Find roster table in HTML comments
    table = None
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if 'id="roster"' in comment:
            comment_soup = BeautifulSoup(comment, "html.parser")
            table = comment_soup.find("table", {"id": "roster"})
            break

    if not table:
        print("❌ Could not find the roster table.")
        continue

    rows = table.tbody.find_all("tr")
    print(f"🔎 Found {len(rows)} player rows.")

    inserted = 0
    for row in rows:
        try:
            cols = row.find_all("td")
            if len(cols) < 9:
                continue

            name = cols[0].text.strip()
            college_raw = cols[7].text.strip()
            birth_raw = cols[8].text.strip()

            if not name or not college_raw or not birth_raw:
                continue

            parts = name.split()
            first_name = parts[0]
            last_name = " ".join(parts[1:])
            college = college_raw.split(",")[-1].strip()
            dob = datetime.strptime(birth_raw, "%m/%d/%Y").strftime("%Y-%m-%d")

            # Check for duplicates
            cursor.execute("""
                SELECT PlayerID FROM Player
                WHERE FirstName = %s AND LastName = %s AND BirthDate = %s
            """, (first_name, last_name, dob))
            if cursor.fetchone():
                print(f"⏭️ Skipping duplicate: {first_name} {last_name}, DOB {dob}")
                continue

            # Insert into Player
            print(f"✅ Inserting: {first_name} {last_name}, DOB {dob}, College {college}")
            cursor.execute("""
                INSERT INTO Player (FirstName, LastName, BirthDate, College)
                VALUES (%s, %s, %s, %s)
            """, (first_name, last_name, dob, college))
            print(f"✅ Inserted: {first_name} {last_name}, DOB {dob}, College {college}")
            inserted += 1

        except Exception as e:
            print(f"⚠️ Error inserting player: {e}")

    inserted_total += inserted
    print(f"📥 Inserted {inserted} players from {abbr.upper()}")

# Finalize
conn.commit()
cursor.close()
conn.close()
print(f"\n✅ Done. Total players inserted: {inserted_total}")