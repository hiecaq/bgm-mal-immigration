from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bgmal',
    use_scm_version=True,
    description='Immigrate watched anime list from Bangumi to MyAnimeList',
    long_description=long_description,
    url='https://github.com/quinoa42/bgm-mal-immigration',
    author='quinoa42',
    author_email='',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='Bangumi, MyAnimeList',
    packages=['bgmal'],
    install_requires=[
        'beautifulsoup4==4.6.0', 'lxml==4.0.0', 'requests==2.18.4'
    ],
    python_requires='>=3.6, <4',
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    entry_points={'console_scripts': ['bgm_mal_immigration=bgmal.cli:main']}
)
