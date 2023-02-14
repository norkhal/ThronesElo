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
url = "https://thrones.tourneygrounds.com/api/v3/tournaments"
page = 1
data = []

# Iterate through the pages
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
    page += 1
    print(f'Processed page {page}')

# Connect to the database
# create the engine
engine = create_engine(connection_string)
print("Connection successful.")
Session = sessionmaker(bind=engine)
session = Session()

# Insert the data into the database
for i, item in enumerate(data):
    session.execute("""
        INSERT INTO tournaments (tjpTournamentID, tournamentName, playerCount, dateEnded, country, region)
        VALUES (:tjpTournamentID, :tournamentName, :playerCount, :dateEnded, :country, :region)
    """, {
        'tjpTournamentID': item['tournament_id'],
        'tournamentName': item['tournament_name'],
        'playerCount': item['player_count'],
        'dateEnded': item['end_time'],
        'country': item['country'],
        'region': item['region']
    })
    if i % 100 == 0:
        print(f'Inserted {i} rows')

# Commit the changes and close the session
session.commit()
session.close()
