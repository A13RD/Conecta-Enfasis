from typing import List
from pydantic import BaseModel

class Programa(BaseModel):
    idPrograma: int
    nombre: str
    lineasEnfasis: List[int]