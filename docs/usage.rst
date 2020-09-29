=====
Usage
=====

Quickstart
===========

To simply use this package, ensure it's been installed and run.

.. code-block:: bash

   json_sorter some_json_file.json


Command line Usage
===================

More complex configurations can be given on the command line.

Python API
============

.. module:: json_sorter
    :synopsis: Sort a JSON file by key without losing organization for nested elements.

Take a :mod:`json` file, sort the keys and insert 4 spaces for indents.

To use json_sorter in a project, begin a python terminal and run.::

    import json_sorter

One Line Solution
-----------------

>>> sorted((json.loads(open('settings.json').read()).items()), key=operator.getitemattr)

You definitely shouldn't implement it as a one liner, *as you can clearly see,*;
however 5 functions and a handful of instantiated classes and debugging, and
we're somehow barely closer to done.

The functions for reading and writing files could be refactored and used over the
entire package.

The logger **should** be set up that way.

This code is going to easily clear 100 lines when a JSON encoded object shouldn't
take more than a few lines to de-serialize and work with.

This'll serve as a good template for testing out tools to build a simple
script with.

The problem is already solved. Let's see what we can't squeeze out of our tools
along the way.

Interestingly enough, this display of excessiveness started as a simple
quick fix.

Originally, this module was used to fix my `<../.vscode/settings.json>`_ from VSCode.

.. automodule:: json_sorter.core
   :members:
   :undoc-members:
   :show-inheritance:

