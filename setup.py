from setuptools import setup

setup(
    name='corpus',
    version='0.1',
    py_modules=['corpus'],
    install_requires=[
        'Click',
        'python-gitlab',
        'sphinx',
    ],
    entry_points='''
        [console_scripts]
        corpus=corpus:cli
    ''',
)
