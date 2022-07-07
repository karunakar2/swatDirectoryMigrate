"""
Tool (script) to update the relative file paths in the ARC-SWAT setup
Initially directed towards SWAT 2012 style databases
karunakar.kintada@gmail.com

The code is self explanatory to an extent even for a non python programmer, so no comments
"""

import sys
import pathlib
import glob

#external module
import pyodbc

if pathlib.Path(__file__).name != 'kSwatMigrate.py':
    #module compatability and .py extension enforcement
    raise Exception ('Rename and run the script as kSwatMigrate.py')
    sys.exit()

if __name__ == '__main__':
    #SWAT version
    swatVer = 'SWAT2012'
    
    #get relavent files, establish access connection
    arcFile = glob.glob('*.mxd')
    tempArcFile = [x.replace('.mxd','') for x in arcFile]

    acsFile = glob.glob('*.mdb')
    knownAcsFiles = ['RasterStore.mdb','SWAT2012.mdb']
    temp = [acsFile.remove(x) for x in knownAcsFiles]
    if any(elem is not None for elem in temp):
        raise Warning ("Some standard files might be missing")
    tempAcsFile = [x.replace('.mdb','') for x in acsFile]

    projFile = list(set(tempArcFile) & set(tempAcsFile)) #pick first
    userReq = input('select current project from \n {}\n  position required: '.format(projFile))
    try:
        if isinstance(int(userReq),int) :
            projFile = projFile[int(userReq)-1]
    except Exception as er:
        print(er)
        print('progressing with {}'.format(projFile[0]))
        projFile = projFile[0]
    
    CNXNSTRING = 'Driver={0};DBQ={1};ExtendedAnsiSQL=1'.format('Microsoft Access Driver (*.mdb)','.'.join((projFile,'mdb')))
    try:
         cnxn   = pyodbc.connect(CNXNSTRING)
         cursor = cnxn.cursor()
    except Exception as err:
        #no debugging here
        print(er)
        raise Exception ('Could not proceed, the SWAT database couldnot be opened')
        sys.exit()

    #the current directory path that goes into the table as an update
    currDir = pathlib.Path().resolve()
    swatFilePath = pathlib.Path('{0}/{1}.{2}'.format(currDir,swatVer,'mdb'))
    try:
        myQuery = "UPDATE MasterProgress SET WorkDir='{0}' WHERE OutputGDB ='{1}';".format(str(currDir),projFile)
        cursor.execute(myQuery)
        if swatFilePath.is_file():
            myQuery = "UPDATE MasterProgress SET SwatGDB='{0}' WHERE OutputGDB ='{1}';".format(swatFilePath,projFile)
            cursor.execute(myQuery)
        else:
            raise Exception ('Cannot locate swat database, {}.mdb'.format(swatVer))
    except Exception as er:
        print(er)
        print('cannot update using queries, please try manually')

    try:
         cnxn.commit()
         cursor.close()
         cnxn.close()
    except Exception as err:
        print(err)
        print('Cannot update the path, try closing the file if already open and do it manually')

    print('Updated, confirm manually if not working')

     
     

 
