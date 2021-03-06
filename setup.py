from setuptools import setup
import os, sys

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if sys.version_info < (3,7):
  sys.exit('Python >= 3.7 is required')

setup(name='DriveBy',
  version='0.1',
  description='Upload specified files to Google drive folder',
  long_description=read('README.md'),
  data_files=[('/etc/driveby', ['etc/config.json'])],
  url='http://github.com/ogelami/DriveBy',
  author='ogelami',
  author_email='robin@forwarddevelopment.se',
  scripts=['bin/driveby'],
  license='MIT',
  packages=['DriveBy'],
  zip_safe=False,
  install_requires=[
    'google-auth',
    'google-api-python-client',
    'google-auth-httplib2',
    'google-auth-oauthlib'])
