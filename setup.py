from setuptools import setup, find_packages


setup(
    name='modeller',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pydantic==1.10.6',
        'SQLAlchemy==2.0.5.post1',
    ],
    python_requires='>=3.11'
)
