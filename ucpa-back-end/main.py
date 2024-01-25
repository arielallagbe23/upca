# Importation des modules FastAPI, Pydantic et autres
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing_extensions import Annotated
from typing import List
from typing import Tuple
import models  # Importation des modèles SQLAlchemy
from database import engine, SessionLocal  # Importation du moteur de la base de données et de la session
from sqlalchemy.orm import Session
from PolishCalculator import PolishCalculator  # Importation du module PolishCalculator
from fastapi.responses import StreamingResponse
from datetime import datetime, timedelta
from sqlalchemy import func 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc
from datetime import date

# Création de l'application FastAPI
app = FastAPI()

# Création des tables dans la base de données
models.Base.metadata.create_all(bind=engine)

# Définition des modèles Pydantic pour les calculs polonais
class PolishCalculBase(BaseModel):
    expression: str

class PolishCalculCreate(PolishCalculBase):
    result: float 

# Appel de la fonction pour obtenir une instance de la base de données (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utilisation d'annotations pour spécifier la dépendance sur la session de la base de données
db_dependency = Annotated[Session, Depends(get_db)]

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
async def make_polish_calcul(polish_calcul: PolishCalculBase, db: db_dependency):

    # Création d'une instance de PolishCalculator
    polish_calculator_instance = PolishCalculator()

    # Calcul de l'expression polonaise
    result = polish_calculator_instance.polish_calcul_npi(polish_calcul.expression)

    # Création d'un enregistrement dans la base de données
    db_polish_calcul = models.PolishCalcul(**polish_calcul.dict(), result=result)
    db.add(db_polish_calcul)
    db.commit()
    db.refresh(db_polish_calcul)

    return db_polish_calcul

# Endpoint pour récupérer tous les resulats et calcules de la base de données
@app.get("/get_all_data/")
async def get_all_data(db: db_dependency, skip: int = 0, limit: int = 10):
    
    # Récupération des données avec pagination
    all_data = db.query(models.PolishCalcul).order_by(desc(models.PolishCalcul.id)).offset(skip).limit(limit).all()

    return all_data

# Endpoint pour exporter les données de la base de données au format CSV
@app.get("/export/csv/")
async def export_csv(start_time: datetime, end_time: datetime, db: db_dependency):
    
    # Récupération des enregistrements dans la plage de temps spécifiée
    records = (
        db.query(models.PolishCalcul)
        .filter(models.PolishCalcul.timestamp.between(start_time, end_time))
        .all()
    )

    # Création du contenu CSV
    csv_content = "expression,result,timestamp\n"
    for record in records:
        csv_content += f"{record.expression},{record.result},{record.timestamp}\n"

    # Définition du nom de fichier CSV
    csv_filename = f"export_historique_calculs.csv"

    # Création de la réponse avec le contenu CSV en streaming
    response = StreamingResponse(content=csv_content, media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={csv_filename}"

    return response

