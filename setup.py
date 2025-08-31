from setuptools import setup, find_packages
from pathlib import Path

# Lee el README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="moonmake",
    version="0.1.50",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "moonmake-new=moonmake.create:__main"
        ]
    },
    install_requires=[
        "requests==2.32.3"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ranon-rat",
    description="Sistema de creación de proyectos con comandos rápidos.",
    url="https://github.com/ranon-rat/moonmake",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
