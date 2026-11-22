
# TP Integrador Backend 1

API REST de una biblioteca desarrollada con Python y FastAPI.

## Funcionalidades
- Crear, consultar y eliminar libros.
- Actualizar libros con PUT y PATCH.
- Filtrar libros por autor y disponibilidad.
- Paginar resultados.
- Buscar libros por título o autor.
- Evitar registros duplicados.
- Guardar y recuperar libros mediante archivos JSON.

## Instalación
Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución
Iniciar el servidor:

```bash
python -m uvicorn main:app --reload
```

Abrir la documentación interactiva:

http://127.0.0.1:8000/docs

## Persistencia
Los libros se guardan automáticamente en datos/libros.json.
La carpeta y el archivo se generan cuando corresponde.
