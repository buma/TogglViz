from setuptools import setup

setup(
        name='TogglViz',
        version='0.1dev',
        author='Marko Burjek',
        packages=['togglviz', ],
        scripts=['bin/fill.py', ],
        license='LICENSE.txt',
        long_description=open('README.txt').read(),
        install_requires=[
            "SQLAlchemy==0.7.9",
            "docopt==0.5.0",
            "schema==0.1.1",
            "python-dateutil==2.1",
        ],

)
