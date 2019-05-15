"""Set up the trying project"""

import os
from setuptools import find_packages
from setuptools import setup

import trying

description = """Python modules often used in dotjab, and elsewhere

Available on guthub and pypi for ease of access
But probably not of great interest to others
"""

def package_files(directory):
    paths = []
    test_extensions = ('.test', '.tests')
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            extension = os.path.splitext(filename)[-1]
            if extension not in test_extensions:
                continue
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('trying')


setup(
    name=trying.__name__,
    packages=find_packages(),
    package_data={'': package_files('trying')},
    version=trying.__version__,
    url=f'https://github.com/jalanb/{trying.__name__}',
    download_url='https://github.com/jalanb/{trying.__name__}/tarball/v{trying.__version__}',
    license='MIT License',
    author='J Alan Brogan',
    author_email='github@al-got-rhythm.net',
    description=description.splitlines()[0],
    long_description=description,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
    ],
    install_requires=['pysyte', 'see'],
    scripts=['bin/try', 'bin/try_files'],
)
