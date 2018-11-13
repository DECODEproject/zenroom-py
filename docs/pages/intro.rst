.. _intro:

Introduction
============

This library contains a very thin Python wrapper for the `Zenroom`_ crypto
virtual machine that has been developed as part of the `DECODE`_ project.

What is DECODE?
---------------

`DECODE`_ is a European Commission funded project exploring and piloting new
technologies that give people more control over how they store, manage and
use personal data generated online. We will test the technology we develop in
two pilot sites and will explore the social benefits of widespread open data
commons.

What is Zenroom?
----------------

`Zenroom`_ is a brand new virtual machine for fast cryptographic operations on
Elliptic Curves. The Zenroom VM has no external dependencies, includes a
cutting edge selection of C99 libraries and builds a small executable ready
to run on: desktop, embedded, mobile, cloud and browsers (webassembly). It
also compiles unikernel (without Linux).

It provides an execution environment for a domain specific language of
cryptographic primitives using a dialect of Lua. The aim of this is to
provide an environment which makes it very easy to write safe encryption
logic, in the form of a Lua script. This script can then be passed into the
Zenroom VM for execution.

For more details of the DSL please see the `Zenroom API documentation`_.

What is this library?
---------------------

This library simply provides a very thin wrapper around the core Zenroom
crypto virtual machine, that aims to make its functionality slightly easier
to use from Python code.

License
-------

This library has currently been released under the `GNU AGPL 3.0 License`_.
This is a strong, free copyleft license published by the Free Software
Foundation in 2007, which is based on the GNU General Public License.

Installation
------------

The package has been published to PyPi, so should be installable via the
following command:

.. code-block:: bash

    $ pip install zenroom

Limitations
-----------

The library includes a static binary containing the Zenroom virtual machine,
compiled for Linux (amd64) systems. As such this library will only work
within this restricted environment.

.. _`Zenroom`: https://zenroom.dyne.org/
.. _`DECODE`: https://decodeproject.eu/
.. _`GNU AGPL 3.0 License`: https://www.gnu.org/licenses/agpl.html
.. _`Zenroom API documentation`: https://zenroom.dyne.org/api/