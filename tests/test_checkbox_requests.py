import pytest
import responses
import requests
from black import CheckCntrl
from server_flask.flask_app import flask_app

class TestCheckbox: 
    c_ch = CheckCntrl(1)

    # @responses.activate
    # def test_mocked_requests():
    #     responses.add( 
    #         responses.GET, "https://example.com/api",
    #         json={"message": "mocked"}, status=200
    #     )

    #     response = requests.get("https://example.com/api")

    #     assert response.status_code == 200
    #     assert response.json() == {"message": "mocked"}

    def test_check_registers(self):
        with flask_app.app_context():
            self.c_ch.test_check_registers() 