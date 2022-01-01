from setuptools import setup

setup(
    name='ticketing',
    packages=['ticketing'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-SQLAlchemy',
        'Flask-WTF'
    ]
)