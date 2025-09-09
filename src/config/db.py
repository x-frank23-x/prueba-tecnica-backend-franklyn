import os
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()
 
DATABASE_URL = os.getenv("DATABASE_URL")

# Validar que exista la URL
if not DATABASE_URL:
    raise ValueError("❌ No se encontró DATABASE_URL en el archivo .env")

# Crear engine global
try:
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True -> logs de SQL
    print("✅ Conexión exitosa a Supabase PostgreSQL")
except SQLAlchemyError as e:
    print("❌ Error al conectar a la base de datos:", str(e))
    raise e


# Crear tablas automáticamente
def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        print("✅ Tablas creadas/verificadas")
    except SQLAlchemyError as e:
        print("❌ Error al crear/verificar tablas:", str(e))
        raise e


# Dependency injection para FastAPI
def get_session():
    with Session(engine) as session:
        yield session
