# Importation des modules SQLAlchemy et datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from datetime import datetime
from database import Base  # Importation de la classe de base pour les modèles SQLAlchemy

# Définition de la classe de modèle PolishCalcul qui représente une table dans la base de données
class PolishCalcul(Base):
    __tablename__ = 'polishcalculs'

    # Définition des colonnes de la table
    id = Column(Integer, primary_key=True, index=True)  # Clé primaire auto-incrémentée
    expression = Column(String(100))  # Chaîne de caractères pour stocker l'expression
    result = Column(Float)  # Valeur flottante pour stocker le résultat du calcul
    timestamp = Column(DateTime, default=func.now())  # Colonne de date et heure avec la valeur par défaut actuelle

# La classe PolishCalcul hérite de la classe Base, définie dans le fichier database.py
# Cela établit une relation avec le moteur de la base de données et fournit des fonctionnalités de mapping ORM
