from libprobe.probe import Probe
from lib.check.selenium import check_selenium
from lib.version import __version__ as version
from lib.probe import register_probe

if __name__ == '__main__':
    checks = {
        'selenium': check_selenium
    }

    probe = Probe("selenium", version, checks)
    register_probe(probe)
    probe.start()
