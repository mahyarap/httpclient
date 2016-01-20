from setuptools import setup, find_packages


setup(
    name = 'httpclient',
    version = '0.1',
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
