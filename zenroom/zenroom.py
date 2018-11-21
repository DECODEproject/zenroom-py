import ctypes
import os.path

zenroom_path = os.path.join(os.path.dirname(__file__), "_zenroom.so")

_zenroom = ctypes.CDLL(zenroom_path)

# Module variable - used to set the max size of the buffer when handling
# zenroom output
__MAX_STRING__ = 4096


class Error(Exception):
    """Base class for Zenroom errors."""

    pass


def execute(script, keys=None, data=None, conf=None, verbosity=1):
    """Invoke Zenroom, capturing and returning the output as a byte string

    This function is the primary method we expose from this wrapper library,
    which attempts to make Zenroom slightly simpler to call from Python. This
    wrapper has only been developed for a specific pilot project within DECODE,
    so beware - the code within this wrapper may be doing very bad things that
    the underlying Zenroom tool does not require.

    Args:
        script (str): Required byte string containing script which Zenroom will execute
        keys (str): Optional byte string containing keys which Zenroom will use
        data (str): Optional byte string containing data upon which Zenroom will operate
        conf (str): Optional byte string containing conf data for Zenroom
        verbosity (int): Optional int which controls Zenroom's log verbosity ranging from 1 (least verbose) up to 3 (most verbose)

    Returns:
            bytes: The output from Zenroom expressed as a byte string
    """
    stdout_buf = ctypes.create_string_buffer(b"\000", __MAX_STRING__)
    stdout_len = ctypes.c_size_t(__MAX_STRING__)
    stderr_buf = ctypes.create_string_buffer(b"\000", __MAX_STRING__)
    stderr_len = ctypes.c_size_t(__MAX_STRING__)

    err = _zenroom.zenroom_exec_tobuf(
        script,
        conf,
        keys,
        data,
        verbosity,
        ctypes.byref(stdout_buf),
        stdout_len,
        ctypes.byref(stderr_buf),
        stderr_len,
    )

    if err != 0:
        raise Error(stderr_buf.value)

    return stdout_buf.value
