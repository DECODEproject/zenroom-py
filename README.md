# zenroom.py

This library provides a very simple wrapper around the Zenroom
(https://zenroom.dyne.org/) crypto virtual machine developed as part of the
DECODE project (https://decodeproject.eu/), that aims to make the virtual
machine easier to call from normal Python code.

This library has been developed for a specific deliverable within the project,
and as such will likely not be suitable for most people's needs. Here we
directly include a binary build of Zenroom compiled only for Linux (amd64), so
any other platforms will be unable to use this library. This library has also
only been tested under Python 3.

Zenroom itself does have good cross platform functionality, so if you are
interested in finding out more about the functionalities offered by Zenroom,
then please visit the website linked to above to find out more.
