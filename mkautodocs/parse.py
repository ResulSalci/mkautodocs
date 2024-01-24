import os
import re
import yaml
import subprocess
from .functions import load_ignore, is_api

mkdocs_nav = ""
module_paths = {}


def parse_project(directory_path, depth=0):
    global mkdocs_nav
    global module_paths

    ignored_paths = load_ignore()

    with os.scandir(directory_path) as entries:

        ignored_files = ("__pycache__", "__init__.py", "__version__.py", "__settings__.py")
        # ignored_files = ["__pycache__", "__init__.py", "__version__.py", "__settings__.py"]

        for entry in entries:

            if directory_path + "/" + entry.name in ignored_paths or entry.name in ignored_files:
                continue

            if os.path.isdir(directory_path + "/" + entry.name):
                mkdocs_nav += (depth + 1) * "    " + (depth > 0) * " " + f"- {entry.name.replace('_', ' ').title()}:\n"
                parse_project(directory_path + "/" + entry.name, depth + 1)

            elif ".py" in entry.name:

                count = 1

                section_name = entry.name.split(".")[0]

                while section_name + "_" + str(count) + ".py" in module_paths:
                    count += 1

                if is_api(directory_path + "/" + entry.name):
                    parse_api(directory_path + "/" + entry.name, count)
                    module_paths[section_name + "_" + str(count) + ".py"] = None
                else:
                    module_paths[section_name + "_" + str(count) + ".py"] = directory_path + "/" + section_name

                mkdocs_nav += (depth + 1) * "    " + (depth > 0) * " " + f"- {section_name.replace('_', ' ').title()}: {section_name}_{count}.md\n"


def parse_api(api_path, count):
    pattern = r'@([a-zA-Z]+)\.(get|post|put|delete)\(".*"(,.*)*\)'

    endpoints = {}

    with open(api_path, "r") as f:
        lines = [line for line in f.read().split("\n") if line.strip()]

    for i, line in enumerate(lines):
        if re.match(pattern, line):
            endpoints[line.split(".")[1].split("(")[0].upper() + " " + (line.split('"')[1])] = \
            lines[i + 1].split("(")[0].split()[-1]

    with open(os.getcwd() + f"\\docs\\{api_path.split('/')[-1].split('.')[0]}_{count}.md", "w") as api_doc:

        for key, value in endpoints.items():
            api_doc.write(f"## {key}\n::: {api_path.split('.')[0].replace('/', '.')}.{value}\n\n")


def modify_yaml(yaml_path, site_name):
    global mkdocs_nav

    if not os.path.exists(yaml_path):
        try:
            subprocess.run(["mkdocs", "new", os.getcwd()], check=True)

        except subprocess.SubprocessError as e:
            print(f"mkdocs encountered a problem: {e}")

    with open(yaml_path, "r") as f:
        yaml_data = yaml.safe_load(f)

    yaml_data["site_name"] = site_name

    yaml_data["plugins"] = 2 * " " + "- search:\n" + \
                           2 * " " + "- mkdocstrings:\n" + \
                           6 * " " + "  default_handler: python\n" + \
                           6 * " " + "  handlers:\n" + \
                           8 * " " + "  python:\n" + \
                           10 * " " + "  options:\n" + \
                           12 * " " + "  heading_level: 2\n" + \
                           12 * " " + "  show_source: false\n" + \
                           12 * " " + "  show_root_toc_entry: false\n" + \
                           12 * " " + "  show_root_full_path: false\n"

    yaml_data["theme"] = 2 * " " + "name: material\n" + \
                         2 * " " + "features:\n" + \
                         4 * " " + "- navigation.tabs\n" + \
                         4 * " " + "- navigation.sections\n" + \
                         4 * " " + "- toc.integrate\n" + \
                         4 * " " + "- navigation.top\n" + \
                         4 * " " + "- search.suggest\n" + \
                         4 * " " + "- search.highlight\n" + \
                         4 * " " + "- content.tabs.link\n" + \
                         4 * " " + "- content.code.annotation\n" + \
                         4 * " " + "- content.code.copy\n" + \
                         2 * " " + "language : en\n" + \
                         2 * " " + "palette:\n" + \
                         4 * " " + "- scheme: default\n" + \
                         6 * " " + "toggle:\n" + \
                         8 * " " + "icon: material/toggle-switch-off-outline\n" + \
                         8 * " " + "name: Switch to dark mode\n" + \
                         6 * " " + "primary: teal\n" + \
                         6 * " " + "accent: purple\n" + \
                         4 * " " + "- scheme: slate\n" + \
                         6 * " " + "toggle:\n" + \
                         8 * " " + "icon: material/toggle-switch\n" + \
                         8 * " " + "name: Switch to light mode\n" + \
                         6 * " " + "primary: teal\n" + \
                         6 * " " + "accent: lime\n"

    yaml_data["nav"] = mkdocs_nav

    yaml_data["markdown_extensions"] = 2 * " " + "- pymdownx.highlight:\n" + \
                                       6 * " " + "anchor_linenums: true\n" + \
                                       2 * " " + "- pymdownx.inlinehilite\n" + \
                                       2 * " " + "- pymdownx.snippets\n" + \
                                       2 * " " + "- admonition\n" + \
                                       2 * " " + "- pymdownx.arithmatex:\n" + \
                                       6 * " " + "generic: true\n" + \
                                       2 * " " + "- footnotes\n" + \
                                       2 * " " + "- pymdownx.details\n" + \
                                       2 * " " + "- pymdownx.superfences\n" + \
                                       2 * " " + "- pymdownx.mark\n" + \
                                       2 * " " + "- attr_list\n"

    with open(yaml_path, "w") as file:
        for key, value in yaml_data.items():
            if key == "site_name":
                file.write(f"{key}: {value}\n")
            else:
                file.write(f"{key}:\n{value}")


def create_mds(docs_directory):
    raw_mds = mkdocs_nav.split("\n")
    mds = []

    if not os.path.exists(docs_directory):
        try:
            subprocess.run(["mkdocs", "new", os.getcwd()], check=True)

        except subprocess.SubprocessError as e:
            print(f"mkdocs encountered a problem: {e}")

    for md in raw_mds:
        if ".md" in md:
            mds.append(md.split()[-1])

    for md in mds:
        if md.replace('.md', '.py') in module_paths and module_paths[md.replace('.md', '.py')] is not None:
            with open(f"{docs_directory}/{md}", "w") as mdf:
                mdf.write(f"::: {module_paths[md.replace('.md', '.py')].replace('/', '.')}")