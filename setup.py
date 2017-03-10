import setuptools

setuptools.setup(
    name="logging-color-formatter",
    version="1.0.0",
    url="https://github.com/leplatrem/logging-color-formatter",

    license='Apache License (2.0)',
    author="Mathieu Leplatre",
    author_email="mathieu@leplat.re",

    description="A colored logging formatter",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),
    zip_safe=True,

    install_requires=["colorama"],
    tests_require=["mock"],

    keywords="logging",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
