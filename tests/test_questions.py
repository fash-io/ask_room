from tests.utils import authorized_client

def test_create_question(client):
    auth_client = authorized_client(client)
    response = auth_client.post("/questions/", json={"title": "What is FastAPI?", "content": "Explain in simple terms."})
    assert response.status_code == 201
    assert response.json()["title"] == "What is FastAPI?"
