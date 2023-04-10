import base64
import os
import random

import pulumi
import pulumi_aws as aws
from pulumi_docker import RegistryImage, RegistryArgs, DockerBuildArgs, Image

CONTEXT = "."

LAMBDA_ROLE = os.environ.get("LAMBDA_ROLE")

LOKI_USER = os.environ.get("LOKI_USER")
LOKI_HOST = os.environ.get("LOKI_HOST")
LOKI_API_KEY = os.environ.get("LOKI_API_KEY")

IMAGE_PLATFORM = "linux/amd64"


def get_ecr_tag():
    return f"ext-{random.randint(100, 999)}"


# Get registry info (creds and endpoint) so we can build/publish to it.
def get_registry_info(rid):
    creds = aws.ecr.get_credentials(registry_id=rid)
    decoded = base64.b64decode(creds.authorization_token).decode()
    parts = decoded.split(':')
    if len(parts) != 2:
        raise Exception("Invalid credentials")
    return RegistryArgs(
        server=creds.proxy_endpoint,
        username=parts[0],
        password=parts[1],
    )


ecr_repository = aws.ecr.Repository(
    "lambda-extension-test-repository",
    tags={"Name": "lambda-extension-test-repository"},
)

registry_info = ecr_repository.registry_id.apply(get_registry_info)

extension_image = Image(
    'lambda-extension-test-extension-image',
    build=DockerBuildArgs(
        context=CONTEXT,
        platform=IMAGE_PLATFORM,
        dockerfile=os.path.join(CONTEXT, "extension.Dockerfile"),
    ),
    image_name=ecr_repository.repository_url.apply(lambda x: f"{x}:ext-1"),
    registry=registry_info,
)

function_handler_image = Image(
    'lambda-extension-test-image',
    build=DockerBuildArgs(
        context=CONTEXT,
        platform=IMAGE_PLATFORM,
        dockerfile=os.path.join(CONTEXT, "handler.Dockerfile"),
    ),
    image_name=ecr_repository.repository_url.apply(lambda x: f"{x}:{get_ecr_tag()}"),
    registry=registry_info,
    opts=pulumi.ResourceOptions(
        depends_on=[
            extension_image,
        ]
    )
)

lambda_function = aws.lambda_.Function(
    "lambda-extension-test",
    description="Lambda function for testing extensions",
    package_type="Image",
    image_uri=function_handler_image.image_name,
    role=LAMBDA_ROLE,
    memory_size=1024,
    timeout=200,
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "LOKI_USER": LOKI_USER,
            "LOKI_API_KEY": LOKI_API_KEY,
            "LOKI_HOST": LOKI_HOST,
        },
    ),
    opts=pulumi.ResourceOptions(
        depends_on=[
            ecr_repository,
            function_handler_image,
        ],
    ),
)
