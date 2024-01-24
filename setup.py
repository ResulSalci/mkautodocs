# setup.py

from setuptools import setup, find_packages

with open("mkautodocs/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mkautodocs',
    version='0.3.4.3',
    packages=find_packages(),
    description='''a python package for documentation''',
    long_description= long_description,
    long_description_content_type="text/markdown",
    package_data={
        'mkautodocs' : ["README.md"]
    },
    install_requires=[
        'mkdocs>=1.5.1',
        'mkdocstrings[python]>=0.22.0',
        'mkdocs-material>=9.1.21',
    ],
    entry_points={
        'console_scripts': [
            'mkautodocs = mkautodocs.cli:main',
        ],
    },
)
