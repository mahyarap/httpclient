from setuptools import setup, find_packages
from httpclient.httpclient import __version__


setup(
    name = 'httpclient',
    version = __version__,
    url = 'https://github.com/mahyarap/httpclient',

    author = 'Mahyar Abbas Pour',
    author_email = 'mahyar.abaspour@gmail.com',
    description = 'An HTTP client',
    license = 'GPLv3',

    packages = ['httpclient'],
    entry_points = {
        'console_scripts': [
            'httpclient = httpclient.httpclient:main',
        ],
    }
)
