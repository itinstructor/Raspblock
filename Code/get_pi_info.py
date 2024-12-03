import platform
import os
import sys


def machine():
    """Return type of machine."""
    if os.name == 'nt' and sys.version_info[:2] < (2, 7):
        return os.environ.get(
            "PROCESSOR_ARCHITEW6432",
            os.environ.get('PROCESSOR_ARCHITECTURE', '')
        )
    else:
        return platform.machine()


def os_bits(machine=machine()):
    """Return bitness ofoperating system, or None if unknown."""
    machine2bits = {'AMD64': 64, 'x86_64': 64, 'i386': 32, 'x86': 32}
    return machine2bits.get(machine, None)


if __name__ == '__main__':
    print(platform.machine())
    print(platform.node())
    print(platform.platform(True))
    print(platform.system())
    print(platform.uname())
    print(platform.architecture())
    print(platform.platform() + ' ' + platform.architecture()[0])
    print(os_bits())
    print(os.name)
