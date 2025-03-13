import pytest
import responses
import requests

@responses.activate
def test_mocked_requests():
    responses.add(
        responses.GET, "https://example.com/api",
        json={"message": "mocked"}, status=200
    )

    response = requests.get("https://example.com/api")

    assert response.status_code == 200
    assert response.json() == {"message": "mocked"}
