# Initial Idea for reproducing passwords.
Initially created for internal use to create reproducible passwords without the need to store them but really whats here is a proof of concept.
As long as the starting seed is secured and there are additional steps to stop repeat tries this should be secure for a lot of applications. Not your bank or your lastpass but ...
This could be adapted for any to allow any service not exposed to the internet.

Is it the most secure, could it be more secure for sure and I can think of ways to do that but for some usecases its useful.


<img src="./images/myscreenshot.png" alt="dsfsdf" width="50%">

# Deploy the code to AWS using Terraform
```
archie@archie passwordendpoints % terraform apply --auto-approve        
data.archive_file.lambda_zip: Reading...
data.archive_file.lambda_zip: Read complete after 0s [id=removed]
aws_api_gateway_api_key.lambda_api_key: Refreshing state... [id=y5l34nt82l]
aws_api_gateway_rest_api.lambda_api: Refreshing state... [id=gcklqwhxg7]
aws_iam_role.lambda_role: Refreshing state... [id=lambda_exec_role]
aws_api_gateway_resource.lambda_resource: Refreshing state... [id=ya79jb]
aws_api_gateway_method.lambda_method: Refreshing state... [id=agm-blah@blah-ya79jb-POST]
aws_iam_role_policy.lambda_cloudwatch_policy: Refreshing state... [id=lambda_exec_role:lambda_cloudwatch_policy]
aws_iam_policy_attachment.lambda_policy: Refreshing state... [id=lambda_policy_attachment]
aws_lambda_function.execute_python: Refreshing state... [id=execute_my_lambda_code]
aws_lambda_permission.apigw_lambda: Refreshing state... [id=terraform-xxxx0000001]
aws_api_gateway_integration.lambda_integration: Refreshing state... [id=agi-blah@blah-ya79jb-POST]
aws_api_gateway_deployment.lambda_deployment: Refreshing state... [id=f3abro]
aws_api_gateway_usage_plan.lambda_usage_plan: Refreshing state... [id=7znbyc]
aws_api_gateway_usage_plan_key.lambda_usage_plan_key: Refreshing state... [id=y5l34nt82l]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no
changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

api_gateway_url = "https://gcklqwhxg7.execute-api.us-east-1.amazonaws.com/dev/execute"
api_key_value = "FpxdJpnBVA1RYEegBMmZwaos50RWGjEJ5qDq0SuB"
archie@archie passwordendpoints
```


# Test api output
Not worried about ssl messages for now.

```
(.venv)archie@archie passwordendpoints % python python_tests.py test this
/Users/archie/PycharmProjects/passwordendpoints/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn(
{
    "password": "cdsfsdf"
}
(.venv)archie@archie passwordendpoints % 
```


# How do I build the podman container

```
podman build -t passwords-app .
```

# Run the container - Not in daemon mode.

```
podman run --rm -p 8000:8000 --env STARTSEED="something juicy" --name my_passwordsapp passwords-app 
```

# Testing the code
```
(.venv) archie@archie passwordendpoints % pytest -v test_code.py
=========================================================================================== test session starts ===========================================================================================
platform darwin -- Python 3.9.6, pytest-8.3.5, pluggy-1.5.0 -- /Users/archie/PycharmProjects/passwordendpoints/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/archie/PycharmProjects/passwordendpoints
plugins: anyio-4.9.0
collected 2 items                                                                                                                                                                                         

test_code.py::test_get_data PASSED                                                                                                                                                                  [ 50%]
test_code.py::test_expected_password PASSED                                                                                                                                                         [100%]

============================================================================================ 2 passed in 0.01s ============================================================================================
(.venv) archie@archie passwordendpoints % 
```
