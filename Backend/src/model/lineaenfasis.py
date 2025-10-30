from typing import List
from pydantic import BaseModel

class LineaEnfasis(BaseModel):
    idLinea: int
    nombre: str
    cursos: List[int] 

    def consultar_cursos(self) -> List[int]:
        """Obtiene la lista de IDs de cursos asociados a la línea."""
        return self.cursos

    def filtrar_semestre(self, semestre: int) -> List[int]:
        """Filtra la lista de cursos por semestre. (Simulado)"""
        print(f"LineaEnfasis {self.nombre} filtrando por semestre {semestre}...")
        if semestre == 20252:
            return [c for c in self.cursos if c != 1002] 
        return self.cursos