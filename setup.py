from setuptools import setup
import pdp

install_requires = []
# eg install_requires = ['urllib3', 'lxml', 'pytest', 'mock', 'tox', 'pyyaml']


setup(name='pdp',
      version=pdp.__version__,
      description='personal data preferences app',
      install_requires=install_requires,
      )
