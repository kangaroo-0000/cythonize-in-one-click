## Cythonize-in-one-click

Currently, classes that extend pydantic's BaseModel is incompatible with Cython.
See: 
https://github.com/samuelcolvin/pydantic/issues/1162

No errors would occur when cythonizing the files. To see the error message, open up the python interpreter in bash, and import the modules using Pydantic.

Use ˋpython setup.py --helpˋ for more info regarding what command lien arguments to be passed.
