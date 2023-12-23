from lambda_src.modules import generate_password
seed = "root" + "archie"
password = generate_password(seed, length=15)
print(password)