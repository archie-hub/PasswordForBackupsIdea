"""dfsdf"""

import json
from modules import generate_password, DEFAULTSEED

def lambda_handler(event, context):# pylint: disable=unused-argument
    """Lambda will accept a username and a hostname"""
    data = json.loads(event.get("body", ""))
    string1 = data.get("string1")
    string2 = data.get("string2")
    seed = string1 + string2
    length = 15

    if not isinstance(length, int) or length <= 0:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid length, must be a positive integer"}),
        }

    password = generate_password(seed, length, DEFAULTSEED)

    return {
        "statusCode": 200,
        "body": json.dumps({"password": password})
    }
