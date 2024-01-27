# Importation des modules FastAPI, Pydantic et autres
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
from typing import Tuple
import mysql.connector
from datetime import datetime
from database import config
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PolishCalculator import PolishCalculator
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse



# Définition des modèles Pydantic pour les calculs polonais
class PolishCalculBase(BaseModel):
    expression: str

class PolishCalculCreate(PolishCalculBase):
    result: float

# Création de l'application FastAPI
app = FastAPI()

# Configuration du middleware CORS pour gérer les requêtes cross-origin
origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Endpoint pour effectuer un calcul polonais et stocker le résultat dans la base de données
@app.post("/calculate/", response_model=PolishCalculCreate, status_code=status.HTTP_201_CREATED)
async def make_polish_calcul(polish_calcul: PolishCalculBase):

    # Création d'une instance de PolishCalculator
    polish_calculator_instance = PolishCalculator()

    # Calcul de l'expression polonaise
    try:
        result = polish_calculator_instance.polish_calcul_npi(polish_calcul.expression)
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": str(e)})

    # Connexion à la base de données avec MySQL Connector
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Exécution d'une requête SQL pour insérer des données
    insert_data_query = "INSERT INTO polishcalculs (expression, result, timestamp) VALUES (%s, %s, %s)"
    data = (polish_calcul.expression, result, datetime.now())

    cursor.execute(insert_data_query, data)

    # Validation les changements dans la base de données
    connection.commit()

    # Fermeture le curseur et la connexion
    cursor.close()
    connection.close()

    return {"expression": polish_calcul.expression, "result": result}

# Endpoint pour récupérer tous les resulats et calcules de la base de données
@app.get("/get_all_data/")
async def get_all_data(skip: int = 0, limit: int = 10):

    # Connexion à la base de données avec MySQL Connector
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Récupération des données avec pagination
    select_data_query = "SELECT id, expression, result FROM polishcalculs ORDER BY id DESC LIMIT %s OFFSET %s"
    
    cursor.execute(select_data_query, (limit, skip))
    all_data = cursor.fetchall()

    # Fermeture le curseur et la connexion
    cursor.close()
    connection.close()
    
    # Création d'une liste de dictionnaires pour une meilleure structure JSON
    data_json = [{"id": item[0], "expression": item[1], "result": item[2]} for item in all_data]

    return JSONResponse(content=data_json)

# Endpoint pour exporter les données de la base de données au format CSV
@app.get("/export/csv/")
async def export_csv(start_time: datetime, end_time: datetime):
    # Connexion à la base de données avec MySQL Connector
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Récupération des enregistrements dans la plage de temps spécifiée
    select_data_query = "SELECT expression, result, timestamp FROM polishcalculs WHERE timestamp BETWEEN %s AND %s"
    cursor.execute(select_data_query, (start_time, end_time))
    records = cursor.fetchall()

    # Fermeture le curseur et la connexion
    cursor.close()
    connection.close()

    # Création du contenu CSV
    csv_content = "expression,result,timestamp\n"
    for record in records:
        csv_content += f"{record[0]},{record[1]},{record[2]}\n"

    # Définition du nom de fichier CSV
    csv_filename = f"export_historique_calculs.csv"

    # Création de la réponse avec le contenu CSV en streaming
    response = StreamingResponse(content=csv_content, media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={csv_filename}"

    return response
