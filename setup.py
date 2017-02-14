from setuptools import setup, find_packages

setup(
  name = 'packtivity-reana-backend',
  version = '0.0.1',
  description = 'packtivity backend for REANA',
  url = '',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  packages = find_packages(),
  include_package_data = True,
  install_requires = [
    'packtivity',
  ],
)
