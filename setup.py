from setuptools import setup

setup(
    name='annealpack',
    version='0.1',
    py_modules=['annealpack'],
    install_requires=[
        'Click',
        'shapely',
        'simanneal',
        'svgpathtools'
    ],
    entry_points='''
        [console_scripts]
        annealpack=annealpack:cli
    ''',
)
