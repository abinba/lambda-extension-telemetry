import os

versions = ["3.7", "3.8", "3.9"]


def get_template() -> str:
    with open("template.Dockerfile", "r") as f:
        template = f.read()
    return template


def generate_dockerfile(template: str, python_version: str):
    folder_name = python_version

    try:
        os.makedirs(folder_name)
    except FileExistsError:
        print(f"Folder: {folder_name} already exists")

    with open(os.path.join(folder_name, "Dockerfile"), "w") as f:
        f.write(template.format(version=python_version))


if __name__ == "__main__":
    docker_template = get_template()
    for version in versions:
        generate_dockerfile(template=docker_template, python_version=version)
