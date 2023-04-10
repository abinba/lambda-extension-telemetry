import os

versions = ["3.7", "3.8", "3.9"]

with open("template.Dockerfile", "r") as f:
    template = f.read()

for version in versions:
    folder_name = version

    try:
        os.makedirs(folder_name)
    except FileExistsError:
        print(f"Folder: {folder_name} already exists")

    with open(os.path.join(folder_name, "Dockerfile"), "w") as f:
        f.write(template.format(version=version))
