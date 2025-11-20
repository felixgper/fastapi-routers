from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix= "/teachers",
                   tags=["teachers"],
                   responses= {404: {"message": "No encontrado"}}
                   )

class Teachers(BaseModel):
    id: int
    name: str
    subject: str
    active: bool

list_teacher = []

@router.get("/")
async def get_teachers():
    if not list_teacher:
        return "LA LISTA DE MAESTROS ESTÁ VACÍA"
    return list_teacher

@router.get("/{id}")
async def get_teachers(id: int):
    existing = search_id(id)
    if existing is None:
        return "NO EXISTE ID DEL PROFESOR"
    return existing

@router.post("/")
async def post_teachers(teacher : Teachers):
    
    existing_teacher = search_id(teacher.id)
    
    if existing_teacher is not None:
        raise HTTPException(status_code= 409, detail= "ID YA EXISTE")
    list_teacher.append(teacher)
    return teacher
    
@router.put("/{id}")
async def put_teachers(id: int, teacher : Teachers):
    
    found = False
    
    for index, value in enumerate(list_teacher):
        if value.id == id:
            list_teacher[index] = teacher
            found = True
            return {"status" : "Profesor Actualizado", "Actualizado" : teacher}
    
    if not found:
        raise HTTPException(status_code= 409, detail= "PROFESOR NO SE PUDO ACTUALIZAR")

@router.delete("/{id}")
async def detele_teachers(id: int):
    
    found = False
    
    for index, value in enumerate(list_teacher):
        if value.id == id:
            del list_teacher[index]
            found = True
            return {"status" : "Profesor Eliminado"}
    
    if not found:
        raise HTTPException(status_code= 409, detail= "PROFESOR NO SE PUDO ELIMINAR")


def search_id(id: int):
    for teacher in list_teacher:
        if teacher.id == id:
            return teacher
    return None