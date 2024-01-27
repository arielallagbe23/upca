import mysql.connector
from database import config  # Importation des paramètres de connexion depuis database.py

# Définition de la classe de modèle PolishCalcul qui représente une table dans la base de données
class PolishCalcul:
    def __init__(self, expression, result):
        self.expression = expression
        self.result = result
        self.timestamp = datetime.now()

def create_polishcalcul_table():
    # Connexion à la base de données avec MySQL Connector
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Exemple de requête pour créer la table (à adapter selon vos besoins)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS polishcalculs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        expression VARCHAR(100),
        result FLOAT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_query)

    # Valider les changements dans la base de données
    connection.commit()

    # Fermer le curseur et la connexion
    cursor.close()
    connection.close()

def insert_polishcalcul(polish_calcul_instance):
    # Connexion à la base de données avec MySQL Connector
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Exécution d'une requête SQL pour insérer des données
    insert_data_query = "INSERT INTO polishcalculs (expression, result, timestamp) VALUES (%s, %s, %s)"
    data = (polish_calcul_instance.expression, polish_calcul_instance.result, polish_calcul_instance.timestamp)

    cursor.execute(insert_data_query, data)

    # Valider les changements dans la base de données
    connection.commit()

    # Fermeture le curseur et la connexion
    cursor.close()
    connection.close()
