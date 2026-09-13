from setuptools import setup, find_packages

setup(
    name="email_package",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    description="Email package",

    author="Rich Lynch",

    license="MIT License",
    install_requires=[
        "email-validator",
        "python-dotenv",
    ],
)