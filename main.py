import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field 

app = FastAPI()
carpeta_datos = Path(__file__).parent / "datos"
archivo_libros = carpeta_datos / "libros.json"
carpeta_datos.mkdir(parents=True, exist_ok=True)

def guardar_libros():
    with open(archivo_libros, "w", encoding="utf-8") as archivo:
        json.dump(libros, archivo, ensure_ascii=False, indent=4)

def cargar_libros():
    if not archivo_libros.exists():
        return []
    try:
        with open(archivo_libros, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if isinstance(datos, list):
            return datos      
    except (OSError, ValueError):
        pass
    return []

#Classe obligatoria para cualquier carga de libros
class LibroEntrada(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)
    autor: str = Field(min_length=3, max_length=60)
    anio: int = Field(ge=1000, le=2100)
    disponible: bool = True

#Clase opcional para actualizar campos de un Libro
class LibroParcial(BaseModel):
    titulo: str | None = Field(default=None, min_length=3, max_length=100)
    autor: str | None = Field(default=None, min_length=3, max_length=60)
    anio: int | None = Field(default=None, ge=1000, le=2100) 
    disponible: bool | None = None 


@app.get("/")
def inicio():
    return {"mensaje": "API de la biblioteca"}


libros = cargar_libros()
siguiente_id = max((libro["id"] for libro in libros), default=0) + 1


@app.get("/libros")
def listar_libros(autor: str | None = None, disponible: bool | None = None,
                  desde: int = 0, limite: int = 100):
    libros_filtrados = libros

    if autor is not None:
        libros_filtrados = [
            libro for libro in libros_filtrados
            if libro["autor"].lower() == autor.lower()
        ]

    if disponible is not None:
        libros_filtrados = [
            libro for libro in libros_filtrados
            if libro["disponible"] == disponible
        ]
    return libros_filtrados[desde:desde + limite]


@app.post("/libros", status_code=201)
def crear_libro(libro: LibroEntrada):
    global siguiente_id
    nuevo_libro = libro.model_dump()
    nuevo_libro["id"] = siguiente_id
    for libro_existente in libros:
        if (
            libro_existente["titulo"].lower() == nuevo_libro["titulo"].lower()
            and libro_existente["autor"].lower() == nuevo_libro["autor"].lower()
        ):
            raise HTTPException(
                status_code=409,
                detail="Datos inválidos: ya existe un libro con el mismo título y autor"
            )

    libros.append(nuevo_libro)
    siguiente_id += 1
    guardar_libros()
    return nuevo_libro


@app.get("/libros/buscar")
def buscar_libros(texto: str):
    resultados = []
    for libro in libros:
        if texto.lower() in libro["titulo"].lower() or texto.lower() in libro["autor"].lower():
            resultados.append(libro)

    return resultados



@app.get("/libros/{id}")
def obtener_libro(id: int):
    for libro in libros:
        if libro["id"] == id:
            return libro

    raise HTTPException(
        status_code=404,
        detail="libro no encontrado" 
    )   


@app.put("/libros/{id}")
def actualizar_libro(id: int, libro_actualizado: LibroEntrada):
    for libro in libros:
        if libro["id"] == id:
            libro.update(libro_actualizado.model_dump())
            guardar_libros()
            return libro

    raise HTTPException(
        status_code=404,
        detail="libro no encontrado"
    )


@app.patch("/libros/{id}")
def actualizar_libro_parcial(id: int, cambios: LibroParcial):
    for libro in libros:
        if libro["id"] == id:
            datos_actualizados = cambios.model_dump(exclude_unset=True)   
            if any(valor is None for valor in datos_actualizados.values()): 
                raise HTTPException(
                    status_code=422,
                    detail="Datos inválidos"
                )
            if datos_actualizados:
                libro.update(datos_actualizados)
            guardar_libros()
            return libro 
        
    raise HTTPException(
        status_code=404,
        detail="libro no encontrado"
    )    



@app.delete("/libros/{id}", status_code=204)
def eliminar_libro(id: int):
    for libro in libros:
        if libro["id"] == id:
            libros.remove(libro)
            guardar_libros()
            return

    raise HTTPException(
        status_code=404,
        detail="libro no encontrado"
    )

 

