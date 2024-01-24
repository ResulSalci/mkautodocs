import os
import re
import subprocess

def create_ignore():

    with open(os.getcwd() + "\\.docignore", "w") as f:
        f.write("")


def load_ignore():

    with open(os.getcwd() + "\\.docignore", "r") as f:
        ignored_paths = f.read().split("\n")

    return ignored_paths


def is_api(file_path):

    pattern = r'@([a-zA-Z]+)\.(get|post|put|delete)\(".*"(,.*)*\)'

    with open(file_path, "r") as f:
        content = f.read()

    lines = content.split("\n")

    for line in lines:
        if re.match(pattern, line):
            return True

    return False

def clear_docs(docs_directory):

    if os.path.exists(docs_directory):
        with os.scandir(docs_directory) as entries:
            for entry in entries:
                if ".md" in entry.name and entry.name != "index.md":
                    os.remove(f"{docs_directory}/{entry.name}")

def build_docs():
    try:
        subprocess.run(["mkdocs", "build"], check=True)
    except subprocess.SubprocessError as e:
        print(f"mkdocs encountered a problem: {e}")

    os.chdir("site")

    with open("Dockerfile", "w") as dockerfile:
        dockerfile.write('FROM nginx:alpine\n\n'
                         'COPY . /usr/share/nginx/html\n\n'
                         'CMD ["nginx", "-g", "daemon off;"]')

    os.chdir("..")
