# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing_extensions import Annotated
from typing import List
from typing import Tuple
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from PolishCalculator import PolishCalculator
from fastapi.responses import StreamingResponse
from datetime import datetime, timedelta
from sqlalchemy import func 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc
from datetime import date


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PolishCalculBase(BaseModel):
    expression: str

class PolishCalculCreate(PolishCalculBase):
    result: float 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

# Add CORS middleware
origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calculate/", response_model=PolishCalculCreate, status_code=status.HTTP_201_CREATED)
async def make_polish_calcul(polish_calcul: PolishCalculBase, db: db_dependency):
    # Créez une instance de votre calculateur PolishCalculator
    polish_calculator_instance = PolishCalculator()

    # Utilisez l'instance pour effectuer le calcul
    result = polish_calculator_instance.polish_calcul_npi(polish_calcul.expression)

    # Enregistrez le calcul dans la base de données
    db_polish_calcul = models.PolishCalcul(**polish_calcul.dict(), result=result)
    db.add(db_polish_calcul)
    db.commit()
    db.refresh(db_polish_calcul)

    # Retournez le résultat avec les valeurs générées automatiquement
    return db_polish_calcul

@app.get("/get_all_data/")
async def get_all_data(db: db_dependency, skip: int = 0, limit: int = 10):
    # Skip the specified number of records and limit the result set
    all_data = db.query(models.PolishCalcul).order_by(desc(models.PolishCalcul.id)).offset(skip).limit(limit).all()

    return all_data

@app.get("/export/csv/")
async def export_csv(start_time: datetime, end_time: datetime, db: db_dependency):
    # Récupérez les enregistrements entre les deux timestamps
    records = (
        db.query(models.PolishCalcul)
        .filter(models.PolishCalcul.timestamp.between(start_time, end_time))
        .all()
    )

    # Créez le contenu CSV
    csv_content = "expression,result,timestamp\n"
    for record in records:
        csv_content += f"{record.expression},{record.result},{record.timestamp}\n"

    # Définissez le nom du fichier CSV
    csv_filename = f"export_{start_time}_{end_time}.csv"

    # Retournez la réponse en streaming avec le contenu CSV
    response = StreamingResponse(content=csv_content, media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={csv_filename}"

    return response
