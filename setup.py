from setuptools import find_packages, setup


setup_args = dict(
    name='gae-testbed',
    version='0.1',
    maintainer='Nick Joyce',
    maintainer_email='nick@boxdesign.co.uk',
    packages=find_packages(),
    namespace_packages=['gae'],
)


if __name__ == '__main__':
    setup(**setup_args)
