import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime

# --- Target Player URL ---
url = "https://www.pro-football-reference.com/players/C/CousKi00/gamelog/2024/#stats"
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'en-US,en;q=0.9'
}

print(f"🔍 Connecting to: {url}")
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    html = response.text
    print("✅ Page fetched successfully.")
except requests.RequestException as e:
    print(f"❌ Connection failed: {e}")
    exit()

# --- Parse and Locate Table ---
soup = BeautifulSoup(html, "html.parser")
table = soup.find("table", {"id": "stats"})
source = "direct HTML"

if not table:
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if 'id="stats"' in comment:
            comment_soup = BeautifulSoup(comment, "html.parser")
            table = comment_soup.find("table", {"id": "stats"})
            if table:
                source = "HTML comment"
                break

if not table:
    print("❌ Could not find the 'stats' table.")
    exit()
print(f"✅ Found 'stats' table in {source}.")

# --- Define mapping to your SQL columns ---
STAT_KEYS = {
    # Game metadata
    'date': 'GameDate',

    # Offensive - Passing
    'pass_att': 'PassingAttempts',
    'pass_cmp': 'PassingCompletions',
    'pass_yds': 'PassingYards',
    'pass_td': 'PassingTDs',
    'pass_int': 'OffensiveInterceptions',
    'fumbles': 'OffensiveFumbles',

    # Offensive - Rushing
    'rush_att': 'RushingAttempts',
    'rush_yds': 'RushingYards',
    'rush_td': 'RushingTDs',

    # Offensive - Receiving
    'rec': 'Receptions',
    'rec_yds': 'ReceivingYards',
    'rec_td': 'ReceivingTDs',

    # Defensive
    'tackles_combined': 'Tackles',
    'sacks': 'Sacks',
    'fumbles_forced': 'ForcedFumbles',
    'def_int': 'DefensiveInterceptions',
    'def_int_yds': 'DefensiveYards',
    'def_int_td': 'DefensiveTDs',

    # Special Teams
    'fgm': 'FieldGoalsMade',
    'fga': 'FieldGoalsAttempted',
    'xpm': 'ExtraPointsMade',
    'xpa': 'ExtraPointsAttempted',
    'punt': 'PuntsAttempted',
    'punt_yds': 'PuntsYards'
}

# --- Initialize season totals (excluding GameDate) ---
totals = {field: 0 for field in STAT_KEYS.values() if field != 'GameDate'}

# --- Process each game row ---
rows = table.find("tbody").find_all("tr")
print(f"\n🧾 Found {len(rows)} rows in <tbody>")

for idx, row in enumerate(rows):
    if row.get("class") and "thead" in row["class"]:
        continue

    print(f"\n📅 Row {idx} — Game Info")
    stat_cells = row.find_all("td")
    if not stat_cells:
        print("⏭️ Skipping row: no stat cells")
        continue

    # Build row_data from data-stat attributes
    row_data = {}
    for cell in stat_cells:
        stat = cell.get("data-stat")
        if stat:
            row_data[stat] = cell.text.strip()

    # Validate date
    date_str = row_data.get("date", "")
    if not date_str or len(date_str) != 10 or '-' not in date_str:
        print(f"❌ Invalid or missing date: '{date_str}' — skipping")
        continue

    try:
        game_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception as e:
        print(f"❌ Failed to parse date '{date_str}': {e}")
        continue

    # Helper to extract values
    def get_stat(stat_name, default=0, cast=int):
        raw = row_data.get(stat_name, '').replace('%', '')
        if raw == '':
            return default
        try:
            return cast(raw)
        except:
            return default

    # Build full stats dictionary
    stats = {'GameDate': game_date}
    for raw_stat, db_field in STAT_KEYS.items():
        cast_type = float if db_field == 'Sacks' else int
        stats[db_field] = get_stat(raw_stat, cast=cast_type)

    # Update totals
    for field, value in stats.items():
        if field in totals:
            totals[field] += value

    # --- Debug Output for Row ---
    print(f"  ✅ Game Date: {stats['GameDate']}")
    print("  📊 Extracted Stats for SQL:")
    for k, v in stats.items():
        if k != 'GameDate':
            print(f"    {k:24}: {v}")

# --- Final Season Totals ---
print("\n📈 SEASON TOTALS:")
for field, total in totals.items():
    print(f"  {field:24}: {total}")