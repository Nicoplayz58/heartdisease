import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()  # Carga las variables desde el .env

# Variables de entorno
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

# Conexión
engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")

# Cargar CSV y guardar en PostgreSQL
df = pd.read_csv("heart.csv")
df.to_sql("heart_data", con=engine, if_exists="replace", index=False)

print("✅ Datos cargados con éxito.")
