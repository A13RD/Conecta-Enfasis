from typing import List
from pydantic import BaseModel
from enum import Enum

class EstadoCurso(str, Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    ACTIVO = "activo"
    FINALIZADO = "finalizado"

class Curso(BaseModel):
    idCurso: int
    nombre: str
    cupo: int
    creditos: int
    cronograma: List[str]
    estado: EstadoCurso

    prerrequisitos: List[int] = [] 
    docente_id: int | None = None

    def validar_cupo(self) -> bool:
        """Verifica si quedan cupos disponibles."""
        return self.cupo > 0

    def aprobar_curso(self):
        """Cambia el estado del curso a aprobado."""
        self.estado = EstadoCurso.APROBADO