def test_get_components_(client):
    print("hello world")
    response = client.get("/api/ping")
    assert 'pong!' in response.json
