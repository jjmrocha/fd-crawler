from distutils.core import setup

setup(
    name='fd-crawler',
    version='1.0.0',
    packages=['fdc', 'fdc.proxy', 'fdc.utils', 'fdc.yahoo', 'fdc.indices'],
    url='https://github.com/jjmrocha/fd-crawler',
    license='MIT',
    author='Joaquim Rocha',
    author_email='jrocha@gmailbox.org',
    description='Finance crawler for reading financial data from public sites'
)
