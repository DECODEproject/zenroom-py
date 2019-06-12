from queue import Empty

from capturer import CaptureOutput

from .zenroom_swig import zenroom_exec_tobuf, zencode_exec_tobuf, zencode_exec_rng_tobuf, zenroom_exec_rng_tobuf
from multiprocessing import Process, Queue


__MAX_STRING__ = 1048576


class ZenroomException(Exception):
    pass


def _sanitize_output(out, err):
    out = out.decode().replace('\x00', '').strip()
    err = err.decode().replace('\x00', '')
    return out, err


def _execute(func, queue, args):
    args['stdout_buf'] = bytearray(__MAX_STRING__)
    args['stderr_buf'] = bytearray(__MAX_STRING__)
    func(*args.values())
    queue.put_nowait(_sanitize_output(args['stdout_buf'], args['stderr_buf']))


def _zen_call(func, arguments):
    with CaptureOutput() as capturer:
        result = Queue()
        p = Process(target=_execute, args=(func, result, arguments))
        p.start()
        p.join()
        p.terminate()

    if result.empty():
        capturer.finish_capture()
        raise ZenroomException(capturer.get_lines())

    return result.get_nowait()


def zencode_exec(script, keys=None, data=None, conf=None, verbosity=1):

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
            tuple: The output from Zenroom expressed as a byte string, the eventual errors generated as a string
    """
    args = dict(script=script, conf=conf, keys=keys, data=data, verbosity=verbosity, stdout_buf=None, stderr_buf=None)
    return _zen_call(zencode_exec_tobuf, args)


def zenroom_exec(script, keys=None, data=None, conf=None, verbosity=1):

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
    args = dict(script=script, conf=conf, keys=keys, data=data, verbosity=verbosity, stdout_buf=None, stderr_buf=None)
    return _zen_call(zenroom_exec_tobuf, args)


def zenroom_exec_rng(script, random_seed, keys=None, data=None, conf=None, verbosity=1):
    args = dict(script=script, conf=conf, keys=keys, data=data, verbosity=verbosity, stdout_buf=None, stderr_buf=None, random_seed=random_seed)
    return _zen_call(zenroom_exec_rng_tobuf, args)


def zencode_exec_rng(script, random_seed, keys=None, data=None, conf=None, verbosity=1):
    args = dict(script=script,
                conf=conf,
                keys=keys,
                data=data,
                verbosity=verbosity,
                stdout_buf=None,
                stderr_buf=None,
                random_seed=random_seed)
    return _zen_call(zencode_exec_rng_tobuf, args)
