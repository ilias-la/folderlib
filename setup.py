import os
from pathlib import Path
from setuptools import setup, find_packages

here = Path(os.path.dirname(__file__)).absolute()

version = {}
with here.joinpath("folderlib/__version__.py").open() as f:
    exec(f.read(), version)

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click',
    'numpy',
    "click_help_colors",
    "coloredlogs",
    "appdirs"
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'pycodestyle', ]

setup(
    name='folderlib',
    version=version['__version__'],
    author="j3di",
    author_email='folderlib@gmail.com',
    license="MIT license",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A Python library for dealing with folder manipulation tasks.",
    entry_points={
        'console_scripts': [
            'folderlib=folderlib.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme,
    keywords='folderlib',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/j3di/folderlib',
    zip_safe=False
)
