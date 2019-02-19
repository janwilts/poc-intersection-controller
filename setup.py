from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='intersection-controller',
    version='0.1.0',
    description='Proof of Concept: Intersection Controller',
    long_description=readme,
    author='Jan Wilts',
    author_email='jan@janwilts.com',
    url='https://github.com/janwilts/poc-intersection-controller',
    install_requires=[
        'paho-mqtt',
        'python-dotenv'
    ],
    packages=find_packages()
)