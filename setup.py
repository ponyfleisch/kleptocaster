from setuptools import setup, find_packages


setup(
    name='kleptocaster',
    version='0.9',
    license='MIT',
    author="Claudio Mettler",
    author_email='github@ponyfleisch.ch',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/ponyfleisch/kleptocaster',
    keywords='Generates RSS feed out of directory of media files.',
    entry_points='''
        [console_scripts]
        kleptocaster=kleptocaster:run
    '''
)