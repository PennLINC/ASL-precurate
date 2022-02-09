from setuptools import setup, find_packages

setup(
    name='asl-precurate',
    version='0.0.1',
    packages=find_packages(include=['asl_precurate', 'asl_precurate.*']),
    install_requires=[
        'requests',
        'importlib; python_version == "3"',
    ],

    entry_points={
        'console_scripts': [
            'asl-precurate=asl_precurate.cli:main'
        ],
    }
)