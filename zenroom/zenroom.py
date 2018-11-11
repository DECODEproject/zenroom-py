from . import _zenroom

def exec(script, keys=None, data=None, conf=None, verbosity=1):
    _zenroom.zenroom_exec(script, conf, keys, data, verbosity)
