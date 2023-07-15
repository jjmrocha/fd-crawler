import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fd-crawler",
    version="0.0.2",
    author="Joaquim Rocha",
    author_email="jrocha@gmailbox.org",
    description="Finance crawler for reading financial data from public sites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjmrocha/fd-crawler",
    packages=setuptools.find_packages(include=['fdc']),
    install_requires=[
        'selenium',
        'requests',
        'python-dateutil',
        'pytz'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
