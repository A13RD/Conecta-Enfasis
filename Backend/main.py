from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from src.controller.auth_controller import AuthController, LoginRequest
from src.controller.estudiante_controller import EstudianteController
from src.controller.coordinador_controller import CoordinadorController, CursoCreate
from src.controller.chatbot_controller import ChatBotController


auth_controller = AuthController()
estudiante_controller = EstudianteController()  
coordinador_controller = CoordinadorController()
chatbot_controller = ChatBotController()

app = FastAPI(
    title="ConectaÉnfasis Backend (Sprint 1)",
    description="Implementación de HU1-HU10 con FastAPI, siguiendo el Modelado UML."
)

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/coordinador")

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Simula la obtención del usuario a partir del token JWT."""
    # En la simulación, el token contiene el rol y el ID
    if "simulated_jwt" in token:
        # Ejemplo: simulated_jwt_for_estudiante1
        parts = token.split('_')
        user_id = parts[-1]
        rol = parts[-2]
        if rol == "coordinador":
             return {"id": 100, "rol": "coordinador"}
        if rol == "estudiante":
             return {"id": 1, "rol": "estudiante"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_coordinador(user: Dict[str, Any] = Depends(get_current_user)):
    if user.get("rol") != "coordinador":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado. Se requiere rol de Coordinador.")
    return user

def get_current_estudiante(user: Dict[str, Any] = Depends(get_current_user)):
    if user.get("rol") != "estudiante":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado. Se requiere rol de Estudiante.")
    return user

# ==============================================================================
# ENDPOINTS DE FASTAPI PARA HU1 - HU10
# ==============================================================================

# ----------------------------------------------------------------------
# HU10: Iniciar sesion con contraseña (Auth)
# ----------------------------------------------------------------------
@app.post("/login/{rol}")
def login(login_data: LoginRequest, rol: str): # 🚨 CAMBIO CRÍTICO AQUÍ: Recibir DTO
    """HU10: Endpoint para iniciar sesión y obtener token."""
    
    # 🚨 PRINT AGREGADO PARA DEBUGGING 🚨
    print(f"DEBUG MAIN: Solicitud POST recibida en /login/{rol} para {login_data.username}")

    # Ahora pasamos los valores del DTO al controlador
    user_auth = auth_controller.login(login_data.username, login_data.password, rol)
    
    if not user_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    return {"message": "Login exitoso", "token": user_auth["token"], "rol": rol}

# ----------------------------------------------------------------------
# HU1 y HU2: Consultar y Filtrar Líneas (Estudiante)
# ----------------------------------------------------------------------
@app.get("/estudiante/lineas", tags=["Estudiante"])
def get_lineas(estudiante: Dict[str, Any] = Depends(get_current_estudiante)):
    """
    HU1: Consulta las líneas de énfasis disponibles para el programa del estudiante.
    Asume que el estudiante autenticado tiene el ID de programa 1.
    """
    # En una aplicación real, 'programa_id' se obtendría del objeto 'estudiante'
    programa_id = 1 
    lineas = estudiante_controller.solicitarLineasEnfasis(programa_id)
    return lineas

@app.get("/estudiante/lineas/filtrar", tags=["Estudiante"])
def filtrar_lineas(semestre: int, estudiante: Dict[str, Any] = Depends(get_current_estudiante)):
    """
    HU2: Filtra las líneas de énfasis por semestre (y devuelve los cursos aprobados).
    """
    programa_id = 1
    cursos_filtrados = estudiante_controller.filtrarLineasPorSemestre(programa_id, semestre)
    
    if not cursos_filtrados:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron cursos aprobados para ese semestre.")
    
    return cursos_filtrados

# ----------------------------------------------------------------------
# HU9: Crear Curso (Coordinador)
# ----------------------------------------------------------------------
@app.post("/coordinador/curso/crear", tags=["Coordinador"])
def crear_curso(curso_data: CursoCreate, coordinador: Dict[str, Any] = Depends(get_current_coordinador)):
    """HU9: Permite al coordinador crear un curso (queda en estado 'pendiente')."""
    curso = coordinador_controller.crear_curso(curso_data)
    if not curso:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al registrar el curso en la base de datos.")
    return {"message": "Curso creado exitosamente. Estado: PENDIENTE", "curso": curso}

# ----------------------------------------------------------------------
# HU4: Aprobar Curso (Coordinador)
# ----------------------------------------------------------------------
@app.put("/coordinador/curso/{curso_id}/aprobar", tags=["Coordinador"])
def aprobar_curso(curso_id: int, coordinador: Dict[str, Any] = Depends(get_current_coordinador)):
    """HU4: Permite al coordinador aprobar un curso pendiente."""
    curso_aprobado = coordinador_controller.aprobarCurso(curso_id)
    if not curso_aprobado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Curso con ID {curso_id} no encontrado o ya aprobado.")
    
    # Simulación de la Notificación (HU6) después de la aprobación
    chatbot_controller.notificar_cambio_hu6(curso_id, f"El curso **{curso_aprobado['nombre']}** ha sido APROBADO y está disponible para inscripción.")
    
    return {"message": "Curso aprobado exitosamente y notificaciones disparadas.", "curso": curso_aprobado}

# ----------------------------------------------------------------------
# HU3, HU5, HU7, HU8: ChatBot (Estudiante)
# ----------------------------------------------------------------------
@app.post("/chatbot/validar_inscripcion", tags=["ChatBot"])
def validar_inscripcion(curso_nombre: str, estudiante: Dict[str, Any] = Depends(get_current_estudiante)):
    """HU3: El chatbot valida cupos y prerrequisitos para un curso."""
    estudiante_id = estudiante.get("id", 1) # Usar ID 1 por defecto en simulación
    mensaje = chatbot_controller.procesar_mensaje_hu3(estudiante_id, curso_nombre)
    return {"respuesta_chatbot": mensaje}

@app.post("/chatbot/inscribir", tags=["ChatBot"])
def inscribir_curso(curso_id: int, estudiante: Dict[str, Any] = Depends(get_current_estudiante)):
    """HU5: Inscribirse en un curso desde el chatbot (integra HU8)."""
    estudiante_id = estudiante.get("id", 1)
    mensaje = chatbot_controller.inscribir_estudiante_hu5(estudiante_id, curso_id)
    return {"respuesta_chatbot": mensaje}

@app.post("/chatbot/solicitar_reporte", tags=["ChatBot"])
def solicitar_reporte(estudiante: Dict[str, Any] = Depends(get_current_estudiante)):
    """HU7: Solicitar reporte consolidado de progreso (integra HU8)."""
    estudiante_id = estudiante.get("id", 1)
    mensaje = chatbot_controller.generar_progreso_hu7(estudiante_id)
    return {"respuesta_chatbot": mensaje}

# ----------------------------------------------------------------------
# HU6: Notificaciones - Endpoint de Prueba (Trigger)
# ----------------------------------------------------------------------
@app.post("/test/notificar_cambio/{curso_id}", tags=["Test_HU6"])
def test_notificar_cambio(curso_id: int, mensaje: str):
    """
    Endpoint de prueba para simular un cambio de cronograma/cupo que dispara HU6.
    """
    notificados = chatbot_controller.notificar_cambio_hu6(curso_id, mensaje)
    return {"message": f"Simulación de cambio en curso {curso_id} completada.", "estudiantes_notificados": notificados}