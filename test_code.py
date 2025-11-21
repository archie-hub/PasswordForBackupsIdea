import pytest
from lambda_src.modules import generate_password
import requests

"""
By the time you see this this the keys will all be invalid and I dont hardcode stuff... putting here for example
Copy and paste the output from terraform below to do a basic test.
Then run 

(.venv) archie@archie passwordendpoints % python python_tests.py test this

but really moved to pytest.
"""

# Example usage
api_gateway_url = "https://fme10u4ey0.execute-api.us-east-1.amazonaws.com/dev/execute"
api_key_value = "test scanner"


def test_get_data():
    assert (
        generate_password(seed="gdg", length=15, defaultseed="blah blah")
        == "R5hY6IMfF5rtmLR"
    )


def test_expected_password():
    assert (
        generate_password(seed="s", length=15, defaultseed="blah blah")
        == "a8paz5yKOt7KUhj"
    )


def test_api_api_blah_blah_seed_UPPER():
    headers = {"Content-Type": "application/json", "x-api-key": api_key_value}
    for i in [("GD", "g"), ("GD", "G"), ("gd", "g")]:
        response = requests.post(
            f"{api_gateway_url}",
            json={"string1": i[0], "string2": i[1]},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json() == {"password": "R5hY6IMfF5rtmLR"}
        assert len(response.json().get("password")) == 15


def test_api_api_blah_blah_seed_try_get():
    headers = {"Content-Type": "application/json", "x-api-key": api_key_value}
    for i in [("GD", "g"), ("GD", "G"), ("gd", "g")]:
        response = requests.get(
            f"{api_gateway_url}",
            json={"string1": i[0], "string2": i[1]},
            headers=headers,
        )
        assert response.status_code == 403
