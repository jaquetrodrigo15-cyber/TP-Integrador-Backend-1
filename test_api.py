
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
