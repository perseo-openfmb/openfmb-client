from setuptools import setup, find_packages

setup(
    name="openfmb-client",            # Nombre para pip
    version="0.3.0",
    description="Cliente Python para interactuar con la API de OpenFMB en microgrids",
    author="Kevin Martinez",
    author_email="kevin9907martinez@gmail.com",
    packages=find_packages(),         # Busca automáticamente la carpeta openfmb_client
    install_requires=[
        "requests>=2.25.0",         # Instalará requests automáticamente
        "pandas"                    # Sugerencia: Si vas a añadir soporte para DataFrames
    ],
    python_requires=">=3.8",
)