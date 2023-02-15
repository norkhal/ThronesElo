import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config

# set our variables from the config file
server = config.server
database = config.database
username = config.username
password = config.password
connection_string = config.connection_string

# Connect to the API
url = "https://thrones.tourneygrounds.com/api/v3/games"
page = 1
data = []

# Keep a dictionary to store the ELO scores for each faction
elo_scores = {}


# Connect to the database
# create the engine
engine = create_engine(connection_string)
print("Connection successful.")
Session = sessionmaker(bind=engine)
session = Session()

# Initialize dictionaries for ELO ratings and win/loss records
elo = {}
wins = {}
losses = {}
entries = {}
k = 10


# Iterate through all available pages
while True:
    try:
        response = requests.get(url, params={'page': page})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        break

    response_data = response.json()
    if len(response_data) == 0:
        break
    data.extend(response_data)
    if (page - 1) % 100 == 0:
        print(f'Retrieved page {page - 1} of data')
    page += 1


# Iterate through each game in the data
for i, item in enumerate(data):
    try:
        p1_id = item['p1_id']
        p1_name = item['p1_name']
        p2_id = item['p2_id']
        p2_name = item['p2_name']
        p1_points = item['p1_points']
        p2_points = item['p2_points']
    except KeyError:
        # Skip iteration if either p1 or p2 data is not found
        continue

    # Check if both players are the same, if so, skip this game
    if p1_id == p2_id:
        continue

    # Initialize ELO and win/loss records for each player if they haven't been seen before
    if p1_id not in elo:
        elo[p1_id] = 1000
        wins[p1_id] = 0
        losses[p1_id] = 0
        entries[p1_id] = 0
    if p2_id not in elo:
        elo[p2_id] = 1000
        wins[p2_id] = 0
        losses[p2_id] = 0
        entries[p2_id] = 0

    # Calculate the ELO rating changes based on the result of the game
    expected_score_p1 = 1 / (1 + 10 ** ((elo[p2_id] - elo[p1_id]) / 400))
    expected_score_p2 = 1 / (1 + 10 ** ((elo[p1_id] - elo[p2_id]) / 400))
    if p1_points == 0:
        elo[p1_id] = elo[p1_id] - k * (0 - expected_score_p1)
        elo[p2_id] = elo[p2_id] + k * (1 - expected_score_p2)
        wins[p2_id] += 1
        losses[p1_id] += 1
    elif p2_points == 0:
        elo[p1_id] = elo[p1_id] + k * (1 - expected_score_p1)
        elo[p2_id] = elo[p2_id] - k * (0 - expected_score_p2)
        wins[p1_id] += 1
        losses[p2_id] += 1

    # Increment the number of entries for both players
    entries[p1_id] += 1
    entries[p2_id] += 1

    # Display progress
    if i % 100 == 0:
        print(f'Processed {i} games')


# Insert the updated ELO ratings, win/loss records, and faction entries into the database
for faction in elo:
    session.execute("""
        INSERT INTO faction (factionName, elo, factionWins, factionLosses, factionEntries)
        VALUES (:factionName, :elo, :factionWins, :factionLosses, :factionEntries)
        """, {
        'factionName': faction,
        'elo': elo[faction],
        'factionWins': wins[faction],
        'factionLosses': losses[faction],
        'factionEntries': entries[faction]
})


# Commit the changes and close the session
session.commit()
session.close()