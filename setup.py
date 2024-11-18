from setuptools import find_packages, setup

setup(
    name='kickstart-autofarm',
    version='0.1',
    description='A onetime setup script for Binghamton EECE project 514\'s raspberry pis',
    url='http://github.com/ecd514/auto-farm',
    author='akapusc1',
    author_email='akapusc1@binghamton.edu',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[

    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
      )
