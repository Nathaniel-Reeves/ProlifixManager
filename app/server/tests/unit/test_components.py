

def test_system_env():
    x = True
    assert x is True

def test_request_example(client):
    print(client)
    response = client.get("/api/ping")
    assert 'ping' in response.json()
