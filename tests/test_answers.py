from tests.utils import authorized_client, create_question, create_answer

def test_post_answer(client):
    auth_client = authorized_client(client)
    question = create_question(auth_client)
    answer = create_answer(auth_client, question_id=question["id"])
    
    assert answer["question_id"] == question["id"]
    assert answer["content"] == "Sample answer."
