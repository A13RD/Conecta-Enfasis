from typing import Dict, Any
from src.controller.db_manager import db_manager
from src.model.curso import Curso, EstadoCurso
from pydantic import BaseModel

class CursoCreate(BaseModel):
    nombre: str
    cupo: int
    creditos: int
    docente_id: int | None = None
  

class CoordinadorController:
    def crear_curso(self, curso_data: CursoCreate) -> Dict[str, Any] | None:
        """HU9: Crear un curso en estado 'pendiente'."""
        # Se usará RETURNING * para obtener los datos del curso recién creado
        query = "INSERT INTO cursos (nombre, cupo, creditos, estado, docente_id) VALUES (:nombre, :cupo, :creditos, :estado, :docente_id) RETURNING *"
        params = {
            "nombre": curso_data.nombre, 
            "cupo": curso_data.cupo, 
            "creditos": curso_data.creditos, 
            "estado": EstadoCurso.PENDIENTE.value, 
            "docente_id": curso_data.docente_id
        }
        
        # db_manager.execute_and_commit ya no soporta RETURNING, 
        # requeriría un cambio al ORM o una consulta separada. Usaremos una simulación simple.
        new_id = db_manager.get_new_id("cursos")
        if db_manager.execute_and_commit(
            "INSERT INTO cursos (idcurso, nombre, cupo, creditos, estado) VALUES (:id, :nombre, :cupo, :creditos, :estado)",
            {"id": new_id, "nombre": curso_data.nombre, "cupo": curso_data.cupo, "creditos": curso_data.creditos, "estado": EstadoCurso.PENDIENTE.value}
        ):
             return db_manager.fetch_one("SELECT * FROM cursos WHERE idcurso = :id", {"id": new_id})
        return None


    def aprobarCurso(self, curso_id: int) -> Dict[str, Any] | None:
        """HU4: Aprobar una oferta de curso."""
        if db_manager.execute_and_commit(
            "UPDATE cursos SET estado='aprobado' WHERE idcurso = :id AND estado != 'aprobado'",
            {"id": curso_id}
        ):
            return db_manager.fetch_one("SELECT * FROM cursos WHERE idcurso = :id", {"id": curso_id})
        return None