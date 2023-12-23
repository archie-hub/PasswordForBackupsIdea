import pytest
from lambda_src.modules import generate_password
import requests

# Example usage
api_gateway_url = "https://gz77c0r82h.execute-api.us-east-1.amazonaws.com/dev/execute"
api_key_value = "REbi4I5tBpUOh9fZ8Xrv8M2AcO2fmeXYwvem3250"


def test_get_data():
    assert (
        generate_password(seed="gdg", length=15, defaultseed="blah blah")
        == "62plsPoS1WuBgRw"
    )


def test_expected_password():
    assert (
        generate_password(seed="s", length=15, defaultseed="blah blah")
        == "WQnoMOEHKl0Sr1t"
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
        assert response.json() == {"password": "62plsPoS1WuBgRw"}
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
