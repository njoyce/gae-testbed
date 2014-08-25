import os.path

from setuptools import find_packages, setup
from setuptools.command import develop


class namespace_develop(develop.develop):
    """
    setuptools does weird things when one namespaced package is installed in
    the environment and this one (which declares the same namespace) fails to
    import correctly after the standard setup.py develop is run.

    To fix this we pseudo install the packages and symlink back to the source
    directories.
    """

    @property
    def namespace_packages(self):
        ns_packages = []

        for pkg in self.distribution.namespace_packages or []:
            pkg = pkg.split('.')

            while pkg:
                ns_packages.append('.'.join(pkg))
                pkg.pop()

        ns_packages = list(map(str, set(ns_packages)))
        ns_packages.sort()

        return ns_packages

    @property
    def nspkg_file(self):
        cmd = self.get_finalized_command('install_egg_info')

        filename, ext = os.path.splitext(cmd.target)

        return '{}-nspkg.pth'.format(filename)

    def get_pth_line(self, pkg):
        parts = tuple(pkg.split('.'))

        line = (
            "import sys,types,os; p = os.path.join({egg_path!r}, *{parts!r});"
            "m = sys.modules.setdefault({pkg!r},types.ModuleType({pkg!r}));"
            "mp = (m or []) and m.__dict__.setdefault('__path__',[]); "
            "(p not in mp) and mp.append(p)"
        )

        args = {
            'egg_path': self.egg_path,
            'parts': parts,
            'pkg': pkg,
        }

        if len(parts) > 1:
            line += "; m and setattr(sys.modules[{root_pkg!r}], {leaf!r}, m)"

            args.update({
                'root_pkg': '.'.join(parts[:-1]),
                'leaf': parts[-1],
            })

        return line.format(**args)

    def install_for_development(self):
        develop.develop.install_for_development(self)

        with open(self.nspkg_file, 'w+') as fp:
            for nspkg in self.namespace_packages:
                pth_line = self.get_pth_line(nspkg)

                fp.write(pth_line + '\n')


setup_args = dict(
    name='gae-testbed',
    version='0.1',
    maintainer='Nick Joyce',
    maintainer_email='nick@boxdesign.co.uk',
    packages=find_packages(),
    namespace_packages=['gae'],
    cmdclass={
        'develop': namespace_develop,
    },
)


if __name__ == '__main__':
    setup(**setup_args)
