from setuptools import setup, find_packages

setup(
    name="dj-inspector",
    version="0.1.0",
    description="A specialized security analysis tool for Django applications",
    author="Gaëtan",
    url="https://github.com/gaetangrond/dj-inspector",
    packages=find_packages(),
    install_requires=["click>=8.1.8,<9.0.0", "rich", "ast"],
    entry_points={
        "console_scripts": [
            "dj-inspector=dj_inspector.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
