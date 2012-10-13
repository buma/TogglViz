from distutils.core import setup

setup(
        name='TogglViz',
        version='0.1dev',
        author='Marko Burjek',
        packages=['togglviz', ],
        license='LICENSE.txt',
        long_description=open('README.txt').read(),
        install_requires=[
            "SQLAlchemy==0.7.9",
        ],

)
