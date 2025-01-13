# Local components
from project_caesar.code import secret_key


if __name__ == "__main__":
    sk = secret_key.generate_secret_key()
    print(f"Generated secret key: {sk}")  # future: use logger here
    print(sk.value)

