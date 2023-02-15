server = 'throneselo.database.windows.net'
database = 'thronesElo_db'
username = 'CloudSAcbbef286'
password = 'BB803N0Sc4AecTkl'
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server'






# connection_string = (f"Driver={{ODBC Driver 18 for SQL Server}};"
#                      f"Server=tcp:{server}.database.windows.net,1433;"
#                      f"Database={database};"
#                      f"Uid={username};"
#                      f"Pwd={password};"
#                      "Encrypt=yes;"
#                      "TrustServerCertificate=no;"
#                      "Connection Timeout=30;")
