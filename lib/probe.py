from libprobe.probe import Probe

_probe: Probe | None = None


def register_probe(probe: Probe):
    global _probe
    _probe = probe


def get_probe() -> Probe:
    if _probe is None:
        raise Exception('probe is None, forget to call register_probe(..)?')
    return _probe
