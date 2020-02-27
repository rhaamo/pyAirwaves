from setuptools import setup

setup(
    name="pyAirwaves",
    version="0.1",
    license="AGPL3",
    python_requires=">=3.6",
    long_description=open("README.md").read(),
    url="https://github.com/rhaamo/pyAirwaves",
    author="Dashie",
    author_email="dashie@sigpipe.me",
    install_requires=[
        "SQLAlchemy",
        "SQLAlchemy-Searchable",
        "SQLAlchemy-Utils",
        "bcrypt",
        "psycopg2-binary",
        "unidecode",
        "texttable",
        "redis",
        "pyais",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov", "jsonschema"],
)
