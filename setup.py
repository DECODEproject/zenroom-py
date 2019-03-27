import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

package_data = [
    "_zenroom_3.5.0.so", "_zenroom_3.5.1.so", "_zenroom_3.5.2.so", "_zenroom_3.5.3.so",
    "_zenroom_3.5.4.so", "_zenroom_3.5.5.so", "_zenroom_3.5.6.so", "_zenroom_3.6.0.so",
    "_zenroom_3.6.1.so", "_zenroom_3.6.2.so", "_zenroom_3.6.3.so", "_zenroom_3.6.4.so",
    "_zenroom_3.6.5.so", "_zenroom_3.6.6.so", "_zenroom_3.6.7.so", "_zenroom_3.6.8.so",
    "_zenroom_3.7.0.so", "_zenroom_3.7.1.so", "_zenroom_3.7.2.so"
]

setuptools.setup(
    name="zenroom",
    version="0.2.0",
    author="Sam Mulube",
    author_email="sam@thingful.net",
    description="Python wrapper for the Zenroom virtual machine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DECODEproject/zenroom-py",
    packages=setuptools.find_packages(),
    package_data={"zenroom": package_data},
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "codecov", "pytest-cov"],
    install_requires=["capturer==2.4"]
)
