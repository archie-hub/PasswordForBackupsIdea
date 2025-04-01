import pytest
from lambda_src.modules import generate_password
import requests

# Example usage
api_gateway_url = "https://fme10u4ey0.execute-api.us-east-1.amazonaws.com/dev/execute"
api_key_value = "7CB3hv6BTraEnB6Qtf4dn9zsc7HW9tpC4lcn1Jlg"


def test_get_data():
    assert (
        generate_password(seed="gdg", length=15, defaultseed="blah blah")
        == "G9mVLHYWWYYjdaK"
    )


def test_expected_password():
    assert (
        generate_password(seed="s", length=15, defaultseed="blah blah")
        == "N7Dt0KTdodf5uwF"
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
        assert response.json() == {"password": "G9mVLHYWWYYjdaK"}
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
