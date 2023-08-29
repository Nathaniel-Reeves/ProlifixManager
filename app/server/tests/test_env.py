def test_system_env():
    x = True
    assert x is True


def test_request_example(client):
    print("hello world")
    response = client.get("/api/ping")
    assert 'pong!' in response.json
