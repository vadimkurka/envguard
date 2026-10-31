from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="envguard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click>=8.0"],
    entry_points={
        "console_scripts": [
            "envguard=envguard.cli:cli",
        ],
    },
    python_requires=">=3.8",
    author="Vadim",
    description="Catch missing, mistyped, and empty environment variables before they break your app.",
    long_description=Path(__file__).with_name("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/vadimkurka/envguard",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
