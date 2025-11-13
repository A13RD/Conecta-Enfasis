from typing import Any, List, Dict
from config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
#import ssl

class DBManager:
    """Clase singleton para manejar la conexión y operaciones de la DB con SQLAlchemy."""

    def __init__(self):
        # 1. Crear el motor de conexión
        try:
            # Usamos la URL completa que ya tiene ?sslmode=require
            self.engine = create_engine(
                settings.DATABASE_URL,
                # 🚨 AJUSTE CRÍTICO: Usamos 'sslmode' en connect_args para asegurar el requisito.
                # psycopg2 maneja el SSL internamente si se le da el parámetro correcto.
                connect_args={"sslmode": "require"} 
            )
            
            # Prueba de conexión
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("✅ DBManager: Conexión exitosa a NeonDB con SQLAlchemy (SSL asegurado).")
        except OperationalError as e:
            print(f"❌ DBManager ERROR: Falló la conexión a NeonDB. Error: {e}")
            self.engine = None
        except Exception as e:
            print(f"❌ DBManager ERROR: Ocurrió un error inesperado al inicializar: {e}")
            self.engine = None

    def fetch_one(self, query: str, params: tuple = ()) -> Dict[str, Any] | None:
        """Ejecuta una consulta y retorna una sola fila."""
        if not self.engine: return None
        try:
            print(f"\n--- DEBUG SQL INICIO ---")
            print(f"QUERY: {query}")
            print(f"PARAMS: {params}")
            print(f"--------------------------\n")
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params).fetchone()
                if result:
                    return dict(result._mapping)
                return None
        except SQLAlchemyError as e:
            print(f"Error en fetch_one: {e}")
            return None

    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Ejecuta una consulta y retorna todas las filas."""
        if not self.engine: return []
        try:
            with self.engine.connect() as connection:
                results = connection.execute(text(query), params).fetchall()
                return [dict(row._mapping) for row in results]
        except SQLAlchemyError as e:
            print(f"Error en fetch_all: {e}")
            return []

    def execute_and_commit(self, query: str, params: tuple = ()) -> bool:
        """Ejecuta un comando (INSERT, UPDATE, DELETE) y hace commit."""
        if not self.engine: return False
        try:
            with self.engine.connect() as connection:
                connection.execute(text(query), params)
                connection.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Error en execute_and_commit: {e}")
            return False
    
    def get_new_id(self, table: str) -> int:
        """Usa la funcionalidad de secuencia de PostgreSQL para ID (simulado/real)."""

        if self.engine:
   
            return 99999 
        return 9999


db_manager = DBManager()