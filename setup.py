from setuptools import setup, find_packages

setup(
    name='tasker',
    version='0.1',
    description='''Are you crazy fan of git? Or maybe you fan of geeky stuff, which you can make with your
                console or terminal? Daily Tracker is thing, which make your dreams come true. 
                It helps you to plan the most important projects and events of your life in style
                of geeks from Silicon Valley.''',
    packages=find_packages(),
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        tasker=tasker.console.main:cli
    ''',
)