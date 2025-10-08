from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import json, os
from threading import Lock

DB_FILE = "estudiante.json"
_file_lock = Lock()

app = FastAPI(
    title="API de Estudiantes",
    description="CRUD de estudiantes utilizando un archivo JSON como base de datos.",
    version="1.0.0",
)

# ----- Modelos -----
class EstudianteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    apellido: str = Field(..., min_length=1, max_length=50)
    aprobado: bool
    nota: float = Field(..., ge=0, le=20)
    fecha: Optional[datetime] = None

class EstudianteOut(EstudianteBase):
    id: int = Field(..., description="Identificador único del estudiante (solo lectura)", frozen=True)


# ----- Utilidades de archivo -----
def _ensure_db_file():
    """Si no existe el archivo, créalo como lista vacía."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def _read_all() -> List[dict]:
    _ensure_db_file()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # si se corrompió, levantamos error legible
            raise HTTPException(500, detail="Error al leer la base de datos (JSON inválido).")
    # por si quedó un dict suelto, lo migramos a lista
    if isinstance(data, dict):
        data = [data]
    return data

def _write_all(items: List[dict]) -> None:
    """Escribe SIEMPRE la lista completa (nunca appends de texto)."""
    tmp = DB_FILE + ".tmp"
    with _file_lock:  # evita condiciones de carrera si haces varias requests rápidas
        with open(tmp, "w", encoding="utf-8") as f:
            # convertimos datetimes a ISO string
            json.dump(items, f, ensure_ascii=False, indent=2, default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o))
        os.replace(tmp, DB_FILE)

def _next_id(items: List[dict]) -> int:
    return (max((it.get("id", 0) for it in items), default=0) + 1)

# ----- Endpoints -----
@app.get("/estudiantes", response_model=List[EstudianteOut], tags=["Estudiantes"])
def listar_estudiantes():
    return _read_all()

@app.get("/estudiantes/{id}", response_model=EstudianteOut, tags=["Estudiantes"])
def obtener_estudiante(id: int = Path(..., ge=1)):
    data = _read_all()
    for it in data:
        if it.get("id") == id:
            return it
    raise HTTPException(404, detail="Estudiante no encontrado")

@app.post("/estudiantes", response_model=EstudianteOut, tags=["Estudiantes"])
def crear_estudiante(payload: EstudianteBase):
    data = _read_all()
    nuevo_id = _next_id(data)
    doc = {
        "id": nuevo_id,
        "nombre": payload.nombre,
        "apellido": payload.apellido,
        "aprobado": payload.aprobado,
        "nota": payload.nota,
        "fecha": (payload.fecha or datetime.utcnow()).isoformat()
    }
    data.append(doc)
    _write_all(data)
    return doc

@app.put("/estudiantes/{id}", response_model=EstudianteOut, tags=["Estudiantes"])
def editar_estudiante(
    id: int = Path(..., ge=1),
    payload: EstudianteBase = ...
):
    data = _read_all()
    for i, it in enumerate(data):
        if it.get("id") == id:
            data[i] = {
                "id": id,
                "nombre": payload.nombre,
                "apellido": payload.apellido,
                "aprobado": payload.aprobado,
                "nota": payload.nota,
                "fecha": (payload.fecha or datetime.utcnow()).isoformat()
            }
            _write_all(data)
            return data[i]
    raise HTTPException(404, detail="Estudiante no encontrado")

@app.delete("/estudiantes/{id}", tags=["Estudiantes"])
def eliminar_estudiante(id: int = Path(..., ge=1)):
    data = _read_all()
    nuevo = [it for it in data if it.get("id") != id]
    if len(nuevo) == len(data):
        raise HTTPException(404, detail="Estudiante no encontrado")
    _write_all(nuevo)
    return {"detail": "Estudiante eliminado"}

