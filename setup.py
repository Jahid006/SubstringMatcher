from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Python based fuzzy substring matcher'
LONG_DESCRIPTION = 'Python based fuzzy substring matcher using fuzzywuzzy and difflib'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="SubstringMatcher", 
        version=VERSION,
        author="Mohammad Jahid",
        author_email="<mohammadjahid1504037@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(include=['SubstringMatcher', 'SubstringMatcher.*']),
        install_requires=['numpy', 'fuzzywuzzy'], 
        
        
        keywords=['python', 'Substring Matcher'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3"
        ]
)