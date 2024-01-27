import mysql.connector

config = {
    'user': 'root',
    'password': 'password',
    'host': 'mysql-db', 
    'port': 3306,
    'database': 'PolishCalculator',
    'raise_on_warnings': True,
}

# Connexion à la base de données
connection = mysql.connector.connect(**config)

# Création d'un curseur pour exécuter des requêtes
cursor = connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS polishcalculs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expression VARCHAR(100),
    result FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

cursor.execute(create_table_query)

# Fermer le curseur et la connexion
cursor.close()
connection.close()
