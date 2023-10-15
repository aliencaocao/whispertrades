from setuptools import setup, find_packages

setup(
    name='whispertrades',
    version='0.1.0',
    description='A Python package for Whispertrades API',
    long_description='A python package for Whispertrades API. Built on pydantic V2 for strict type checking, and requests for HTTP requests. Requires Python 3.8+',
    author='Billy Cao',
    author_email='aliencaocao@gmail.com',
    url='https://github.com/aliencaocao/whispertrades',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic>=2.0',
        'orjson',
        'requests-ratelimiter'
    ],
    python_requires='>=3.8',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)