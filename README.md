## Cythonize-in-one-click

Currently, classes that extend pydantic's BaseModel is incompatible with Cython.
See: 
https://github.com/samuelcolvin/pydantic/issues/1162

No errors would occur when cythonizing the files, however. To see the error message, open up the python interpreter in bash, and import modules that uses Pydantic.

Use `python setup.py --help ` for more info regarding what command line arguments to be passed.
