def test_search_by_filename(client):
    response = client.get("/v1/search", params={"file_name": "sample"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
