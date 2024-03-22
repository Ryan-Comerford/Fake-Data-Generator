from setuptools import setup, find_packages

setup(
    name="MythosMaker",
    version="0.0.3",
    author="Ryan William Comerford",
    author_email="comerford.ryan31@gmail.com",
    description="A simple package to generate fake data",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/Ryan-Comerford/Fake-Data-Generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "importlib",
        "random",
        "sqlalchemy",
        "faker",
        "multiprocessing",
        "string",
        "datetime",
        "numpy"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
