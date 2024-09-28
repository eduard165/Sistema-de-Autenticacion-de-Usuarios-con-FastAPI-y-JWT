import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.mongo import connect_to_mongo, close_mongo_connection

@pytest.fixture(scope="module")
def test_client():
    # Inicializar conexión a MongoDB antes de las pruebas
    pytest.run_loop = pytest.mark.asyncio
    async def initialize_db():
        await connect_to_mongo()

    async def teardown_db():
        await close_mongo_connection()

    app.on_event("startup")(initialize_db)
    app.on_event("shutdown")(teardown_db)
    
    with TestClient(app) as client:
        yield client
