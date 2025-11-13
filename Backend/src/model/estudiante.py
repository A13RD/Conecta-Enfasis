from typing import List
from pydantic import BaseModel

class Estudiante(BaseModel):
    id: int
    nombre: str
    contraseña: str
    programa: int
    cursos: List[int] 


    def consultar_cursos(self) -> List[int]:
        """Retorna la lista de IDs de cursos inscritos."""
        return self.cursos

    def inscribirse(self, curso_id: int) -> bool:
        """Añade un curso a la lista de inscritos (lógica en Controller)."""
        return True

    def cancelar_curso(self) -> bool:
        """Pone el curso en estado cancelado (pass para Sprint 1)."""
        pass