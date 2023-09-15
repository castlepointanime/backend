import os
from dotenv import load_dotenv


load_dotenv('../backend.env')


def load_env(input: str) -> str:
    data = os.getenv(input)
    assert type(data) == str and len(data) > 0, f"Invalid or no '{input}' environment variable."
    return data


COGNITO_REGION: str = load_env("COGNITO_REGION")
COGNITO_USERPOOL_ID: str = load_env("COGNITO_USERPOOL_ID")
COGNITO_APP_CLIENT_ID: str = load_env("COGNITO_APP_CLIENT_ID")
AWS_ACCESS_KEY_ID: str = load_env("AWS_ACCESS_KEY_ID") # TODO this should be accessed only with the ~/.aws/credentials file, not directly in the backend
AWS_SECRET_ACCESS_KEY: str = load_env("AWS_SECRET_ACCESS_KEY") # TODO this should be accessed only with the ~/.aws/credentials file, not directly in the backend
AWS_SESSION_TOKEN: str = load_env("AWS_SESSION_TOKEN") # TODO see above
MONGO_URI: str = load_env("MONGO_URI")
MONGO_DB_NAME: str = load_env("MONGO_DB_NAME")
DOCUSIGN_CLIENT_ID: str = load_env("DOCUSIGN_CLIENT_ID")
DOCUSIGN_IMPERSONATED_USER_ID: str = load_env("DOCUSIGN_IMPERSONATED_USER_ID")
DOCUSIGN_PRIVATE_KEY: str = load_env("DOCUSIGN_PRIVATE_KEY")
CONTRACT_TEMPLATE_ID: str = load_env("CONTRACT_TEMPLATE_ID")
