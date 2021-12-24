from setuptools import setup

setup(
    name="rednit.py",
    version="1.0.0",
    license="Apache Software License",
    description="comprehensive and feature rich wrapper for the Tinder API",
    author="Kaktushose",
    author_email="faulie50@gmail.com",
    url="https://github.com/rednit-team/tinder.py",
    keywords="tinder tinder-api rest-api api wrapper api-client library framework",
    install_requires=["requests"],
    long_description_content_type="text/markdown",
    long_description=open("./README.md", "rt").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
