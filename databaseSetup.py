import config
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

# set our variables from the config file
server = config.server
database = config.database
username = config.username
password = config.password
connection_string = config.connection_string

print("configuration variables loaded")


# Create a new base class for the tables
Base = declarative_base()
print("Created a new base class")


# Define the table structure
class Players(Base):
    __tablename__ = 'players'
    playerID = Column(Integer, primary_key=True)
    tjpPlayerID = Column(Integer)
    playerName = Column(String)
    entries = Column(Integer)
    elo = Column(Integer)
    wins = Column(Integer)
    loses = Column(Integer)
    dateCreated = Column(DateTime)


print("Defined the player table structure")


class FactionAgenda(Base):
    __tablename__ = 'factionAgenda'
    deckID = Column(Integer, primary_key=True)
    factionID = Column(Integer)
    agendaID = Column(Integer)
    dateCreated = Column(DateTime)
    elo = Column(Integer)
    factionAgendaWins = Column(Integer)
    factionAgendaLosses = Column(Integer)
    factionAgendaEntries = Column(Integer)


print("Defined the faction agenda table structure")


class Faction(Base):
    __tablename__ = 'faction'
    factionID = Column(Integer, primary_key=True)
    factionName = Column(String)
    elo = Column(Integer)
    factionWins = Column(Integer)
    factionLosses = Column(Integer)
    factionEntries = Column(Integer)


print("Defined the faction table structure")


class Agenda(Base):
    __tablename__ = 'agenda'
    agendaID = Column(Integer, primary_key=True)
    agendaName = Column(String)
    elo = Column(Integer)
    agendaWins = Column(Integer)
    agendaLosses = Column(Integer)
    agendaEntries = Column(Integer)


print("Defined the agenda table structure")


class Tournaments(Base):
    __tablename__ = 'tournaments'
    tournamentID = Column(Integer, primary_key=True)
    tjpTournamentID = Column(Integer)
    tournamentName = Column(String)
    dateEnded = Column(DateTime)
    country = Column(String)
    region = Column(String)
    playerCount = Column(Integer)


print("Defined the tournament table structure")


class TournamentRounds(Base):
    __tablename__ = 'tournamentRounds'
    tournamentRoundID = Column(Integer, primary_key=True)
    tjpGameID = Column(Integer)
    tournamentID = Column(Integer)
    roundNumber = Column(Integer)
    topCut = Column(Integer)
    isDraw = Column(Boolean)
    winnerID = Column(Integer)
    winnerFactionID = Column(String)
    winnerAgendaID = Column(Integer)
    loserID = Column(Integer)
    loserFactionID = Column(String)
    loserAgendaID = Column(Integer)
    player1ID = Column(Integer)
    player1StartElo = Column(Integer)
    player1EndElo = Column(Integer)
    player2ID = Column(Integer)
    player2StartElo = Column(Integer)
    player2EndElo = Column(Integer)
    winnerFactionAgendaStartElo = Column(Integer)
    winnerFactionAgendaEndElo = Column(Integer)
    loserFactionAgendaStartElo = Column(Integer)
    loserFactionAgendaEndElo = Column(Integer)
    winnerAgendaStartElo = Column(Integer)
    winnerAgendaEndElo = Column(Integer)
    loserAgendaStartElo = Column(Integer)
    loserAgendaEndElo = Column(Integer)
    winnerFactionStartElo = Column(Integer)
    winnerFactionEndElo = Column(Integer)
    loserFactionStartElo = Column(Integer)
    loserFactionEndElo = Column(Integer)

print("Defined the tournament round table structure")


# create the engine
engine = create_engine(connection_string)
print("Connection successful.")


# create the tables
Base.metadata.create_all(engine)
print("Tables created.")


# Create the table in the database
# Base.metadata.create_all(engine)
# print("Created the database tables")
