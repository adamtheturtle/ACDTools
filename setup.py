"""
Setup script for DC/OS End to End tests.
"""

from setuptools import setup

setup(
    name='Plex Tools',
    author='Adam Dangoor',
    author_email='adamdangoor@gmail.com',
    install_requires=['click', 'PyYAML'],
    entry_points="""
        [console_scripts]
        plex-tools=acdtools:plex_tools
    """,
)
