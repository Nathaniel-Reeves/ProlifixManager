def test_test():
    print("WORKED")

def test_request_example(client):
    response = client.get("/ping")
    print(response)
    assert 'pong!' in response.json()
