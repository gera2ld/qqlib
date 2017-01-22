from setuptools import setup, find_packages

setup(
    name='qqlib',
    version='1.0.0',
    description='QQ library for Python.',
    long_description='QQ library for Python, based on web APIs.',
    url='https://github.com/gera2ld/qqlib',
    author='Gerald',
    author_email='i@gerald.top',
    license='MIT',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='qq',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'rsa',
        'requests',
    ],
)
