import subprocess
from mkautodocs import parse, functions
import argparse
import os

def parse_project(directory_name, site_name):
    parse.parse_project(directory_name)
    parse.modify_yaml(os.getcwd() + "\\mkdocs.yml", site_name)
    parse.create_mds(os.getcwd() + "\\docs")


def create_and_parse(directory_name, site_name):
    try:
        subprocess.run(["mkdocs", "new", os.getcwd()], check=True)
        functions.create_ignore()
        parse_project(directory_name, site_name)


    except subprocess.SubprocessError as e:
        print(f"mkdocs encountered a problem: {e}")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sitename", help="name of the documentation site",default="my site")
    parser.add_argument("command", choices=["scan", "new", "build", "v"], help="Command to execute")
    parser.add_argument("directory_name", nargs="*", default=os.getcwd(), help="Main directory of all projects to document")
    args = parser.parse_args()

    if not args.command:
        print("Please enter a command to execute")

    else:
        if not args.directory_name:
            print("Please specify the directory that you want to start parsing")

        else:
            if args.command == "scan":
                functions.clear_docs(os.getcwd() + "\\docs")
                parse_project(args.directory_name[0], args.sitename)

            elif args.command == "new":
                functions.clear_docs(os.getcwd() + "\\docs")
                create_and_parse(args.directory_name[0], args.sitename)

            elif args.command == "build":
                functions.build_docs()

            elif args.command == "v":
                from mkautodocs import __version__; print("current version is :" + __version__)


if __name__ == "__main__":
    main()
