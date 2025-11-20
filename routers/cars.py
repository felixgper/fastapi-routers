from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix= "/cars",
                   tags=["cars"],
                   responses= {404: {"message": "No encontrado"}}
                   )

class Cars(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    available: bool
    
list_cars = []

@router.get("/")
async def get_cars():
    if not list_cars:
        return "LA LISTA DE CARROS ESTÁ VACÍA"
    return list_cars

@router.get("/{id}")
async def get_cars(id: int):
    if search_id(id) is None:
        return "NO SE ENCONTRO EL ID DEL CARRO"
    return search_id(id)

@router.post("/")
async def post_cars(car : Cars):
    
    existing = search_id(car.id)
    
    if existing is not None:
        raise HTTPException(status_code= 409, detail= "YA EXISTE EL ID DEL CARRO")
    list_cars.append(car)
    return car

@router.put("/{id}")
async def put_cars(id: int, car: Cars):
    
    found = False
    
    for index, value in enumerate(list_cars):
        if value.id == id:
            list_cars[index] = car
            found = True
            return {"status" : "CARRO ACTUALIZADO", "actualizado": car}
    
    if not found:
        raise HTTPException(status_code= 409, detail= "NO SE PUDO ACTUALIZAR")
    
@router.delete("/{id}")
async def delete_cars(id: int):
    
    found = False
    
    for index, value in enumerate(list_cars):
        if value.id == id:
            del list_cars[index]
            found = True
            return {"status" : "CARRO ELIMINADO"}
    
    if not found:
        raise HTTPException(status_code= 409, detail= "NO SE PUDO ELIMINAR")

def search_id(id : int):
    for car in list_cars:
        if car.id == id:
            return car
    return None