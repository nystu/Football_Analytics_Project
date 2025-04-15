LOG_FILE = "slug_failures.log"
cutoff_player_id = 253  # This is the last PlayerID you want to keep

# --- Trim the log file after a specific PlayerID ---
with open(LOG_FILE, "r") as file:
    lines = file.readlines()

# Keep lines only until the one that contains the cutoff PlayerID
new_lines = []
for line in lines:
    new_lines.append(line)
    if f"PlayerID: {cutoff_player_id} " in line:
        break  # Stop collecting lines after we find PlayerID 253

# Overwrite the file with the trimmed content
with open(LOG_FILE, "w") as file:
    file.writelines(new_lines)

print(f"✅ Log trimmed after PlayerID {cutoff_player_id}")