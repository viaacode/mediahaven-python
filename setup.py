from setuptools import find_packages, setup

setup(
    name="mediahaven",
    version="0.8.0",
    license="GPL",
    author="Mattias",
    author_email="mattias.poppe@meemoo.be",
    packages=find_packages(exclude=["tests"]),
    long_description=open("README.md", encoding="utf8").read(),
    zip_safe=False,
    setup_requires=["wheel"],
    install_requires=["oauthlib==3.1.0", "requests_oauthlib==1.3.0", "requests"],
)
