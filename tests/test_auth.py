def test_register(client):
    response = client.post("/auth/register", json={"email": "newuser@test.com", "password": "123456"})
    assert response.status_code == 201

def test_login(client):
    client.post("/auth/register", json={"email": "loginuser@test.com", "password": "123456"})
    response = client.post("/auth/login", data={"username": "loginuser@test.com", "password": "123456"})
    assert response.status_code == 200
    assert "access_token" in response.json()
