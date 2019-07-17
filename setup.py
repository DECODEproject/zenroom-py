import setuptools
import os
import sys

VERSION="1.0.6"

if sys.argv[-1] == 'publish':
    os.system(f"git tag -a {VERSION}")
    os.system(f"git push origin {VERSION}")
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zenroom",
    version=VERSION,
    author="Sam Mulube",
    author_email="sam@thingful.net",
    maintainer="Puria Nafisi Azizi",
    maintainer_email="puria@dyne.org",
    description="Python wrapper for the Zenroom virtual machine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DECODEproject/zenroom-py",
    packages=setuptools.find_packages(),
    package_data={"zenroom": ["libs/Linux/**/**", "libs/Darwin/**/**"]},
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "codecov", "pytest-cov"],
    install_requires=["capturer==2.4"],
    python_requires=">=3.5",
    project_urls={
            'Zenroom': 'https://zenroom.dyne.org',
            'DECODE': 'https://decodeproject.eu',
    },
    entry_points={
        "console_scripts": [
            "zenroom-test = tests.zenroom_cli_test:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Security"
      ],
)
