from setuptools import find_packages, setup

setup(
    name='whispertrades',
    version='0.1.2',
    description='A Python package for Whispertrades API',
    long_description='A python package for Whispertrades API. Built on pydantic and requests. Requires Python 3.8+.',
    author='Billy Cao',
    author_email='aliencaocao@gmail.com',
    maintainer='Billy Cao',
    maintainer_email='aliencaocao@gmail.com',
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
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    project_urls={
        "Documentation": "https://whispertrades.readthedocs.io/",
        "Issues": "https://github.com/aliencaocao/whispertrades/issues",
        "Releases": "https://github.com/aliencaocao/whispertrades/releases",
        "Source Code": "https://github.com/aliencaocao/whispertrades",
    },
    license='Apache 2.0',
    keywords='whispertrades api python'
)