# Importation des modules nécessaires de SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Définition de l'URL pour la connexion à la base de données MySQL
# Format : 'mysql+mysqlconnector://nom_utilisateur:mot_de_passe@hôte:port/nom_base_de_données'
URL_DATABASE = 'mysql+mysqlconnector://root:root@localhost:8889/PolishCalculator'

# Création d'un moteur SQLAlchemy qui gérera la connexion à la base de données
engine = create_engine(URL_DATABASE)

# Création d'un sessionmaker qui sera utilisé pour créer des sessions pour interagir avec la base de données
# autocommit=False : Les transactions ne sont pas validées automatiquement
# autoflush=False : Les objets ne sont pas écrits automatiquement dans la base de données
# bind=engine : Association du sessionmaker au moteur de la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création d'une classe de base pour les définitions de classes déclaratives
# Cette classe de base sera utilisée comme fondation pour vos classes ORM (Object-Relational Mapping)
Base = declarative_base()


