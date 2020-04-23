@echo off
call "c:\program files\QGIS 3.10\bin\o4w_env.bat"
call "c:\program files\QGIS 3.10\bin\qt5_env.bat"
call "c:\program files\QGIS 3.10\bin\py3_env.bat"

@echo on
pyrcc5 -o resources.py resources.qrc