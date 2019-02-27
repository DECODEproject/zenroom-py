import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zenroom",
    version="0.1.0",
    author="Sam Mulube",
    author_email="sam@thingful.net",
    description="Python wrapper for the Zenroom virtual machine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DECODEproject/zenroom-py",
    packages=setuptools.find_packages(),
    package_data={"zenroom": ["_zenroom_3_5.so", "_zenroom_3_7.so", "_zenroom_3_6.so"]},
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=["capturer==2.4"]
)
