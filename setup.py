# coding: utf8

from setuptools import setup


setup(
    name="prometheus",
    version="0.1",
    description="dockerized CI script",
    author="Liu Zhuo",
    author_email="zliu@thoughtworks.com",
    url="https://github.com/ThoughtWorksInc/prometheus",
    packages=["prometheus"],
    entry_points={
        "console_scripts": ["prometheus = prometheus.prometheus:main"]
    },
    install_requires=[
        "docker-py"
    ]
)
