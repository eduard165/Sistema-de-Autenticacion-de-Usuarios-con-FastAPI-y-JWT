def test_register_user(test_client):
    # Prueba para registrar un nuevo usuario
    response = test_client.post(
        "/users/register/",
        json={"username": "usuario_test", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Usuario registrado exitosamente"}

def test_login_for_access_token(test_client):
    # Prueba para obtener el token de acceso
    response = test_client.post(
        "/users/token/",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_current_user(test_client):
    # Primero obtenemos el token
    response = test_client.post(
        "/users/token/",
        data={"grant_type":"password","username": "test@example.com", "password": "password123"},
    )
    token = response.json()["access_token"]

    # Luego hacemos una petición a /me con el token
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get("/users/me/", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
