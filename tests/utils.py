def create_user(client, email="user@test.com", password="123456"):
    response = client.post("/auth/register", json={"email": email, "password": password})
    return response

def login_user(client, email="user@test.com", password="123456"):
    response = client.post("/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]

def authorized_client(client, email="user@test.com", password="123456"):
    create_user(client, email, password)
    token = login_user(client, email, password)
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

def create_question(client, title="Test Title", content="Test content."):
    response = client.post("/questions/", json={"title": title, "content": content})
    return response.json()

def create_answer(client, question_id: int, content="Sample answer."):
    response = client.post("/answers/", json={"question_id": question_id, "content": content})
    return response.json()
