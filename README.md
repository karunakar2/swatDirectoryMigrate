# swatDirectoryMigrate
Sometimes the ARC SWAT projects are built elsewhere and used on different windows machines. Traditionally, the databases need some updates. This is an attempt to automate it and centralise for multiple versions. Bear with python.  Thanks

Please check this thread:
'Moving SWAT working files to another computer'
at https://groups.google.com/g/arcswat/c/cyShln8LqCA

Run this script in the directory where you've copied your SWAT setup files to.

Scope:
1. Currently devised for SWAT2012 and windows use (others not tested)

Dependencies:
1. Needs an external pyodbc module (pip install pyodbc) or equivalent conda env.
2. This file is used in a module, so name might be a restriction at the moment.

Changes welcome.
Please merge changes if you fork for a single window update to endusers.

Karunakar
