# zenroom.py

This library attempts to provide a very simple wrapper around the Zenroom
(https://zenroom.dyne.org/) crypto virtual machine developed as part of the
DECODE project (https://decodeproject.eu/), that aims to make the Zenroom
virtual machine easier to call from normal Python code.

This library has been developed for a specific deliverable within the project,
and as such will likely not be suitable for most people's needs. Here we
directly include a binary build of Zenroom compiled only for Linux (amd64), so
any other platforms will be unable to use this library. This library has also
only been tested under Python 3.

Zenroom itself does have good cross platform functionality, so if you are
interested in finding out more about the functionalities offered by Zenroom,
then please visit the website linked to above to find out more.

## Installation

The package can be installed by running:

```bash
$ pip install zenroom
```

**NOTE - the above command attempts to install the zenroom package, pulling in
the Zenroom VM as a precompiled binary, so will only work on Linux (amd64)
machines.**

