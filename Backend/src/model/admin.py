from pydantic import BaseModel

class Admin(BaseModel):
    id: int
    nombre: str
    contraseña: str

    def consultar_auditoria(self):
        pass

    def gestionar_usuarios(self):
        pass