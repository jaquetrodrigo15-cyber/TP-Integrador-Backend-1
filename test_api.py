
from fastapi.testclient import TestClient
from main import app

cliente = TestClient(app)


def test_inicio():
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"mensaje": "API de la biblioteca"}


def test_busqueda_sin_texto():
    respuesta = cliente.get("/libros/buscar")
    assert respuesta.status_code == 422


def test_libro_inexistente():
    respuesta = cliente.get("/libros/999999")
    assert respuesta.status_code == 404

def test_paginacion(monkeypatch):
    import main

    libros_prueba = [
        {"id": 1, "titulo": "Libro Uno", "autor": "Autor Uno", "anio": 2001, "disponible": True},
        {"id": 2, "titulo": "Libro Dos", "autor": "Autor Dos", "anio": 2002, "disponible": True},
        {"id": 3, "titulo": "Libro Tres", "autor": "Autor Tres", "anio": 2003, "disponible": False},
    ]

    monkeypatch.setattr(main, "libros", libros_prueba)

    respuesta = cliente.get("/libros?desde=1&limite=2")

    assert respuesta.status_code == 200
    assert [libro["id"] for libro in respuesta.json()] == [2, 3]