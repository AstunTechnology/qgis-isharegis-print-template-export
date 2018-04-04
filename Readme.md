# iShareGIS QGIS Print Composer template exporter #
## Introduction ##
This is a QGIS plugin which is used to convert the selected QGIS Print Composer template to an iShareGIS print template.
## Requirements ##
* QGIS 2 (tested with 2.18.18)
* An Astun Services account

## Installation ##
* Extract the zip file
* Copy the iShareGISPrintTemplateExport directory to the QGIS Python plugin directory
  * (`C:\Users\{username}\.qgis2\python\plugins\` on Windows)

## Set up ##
Setup is initially done on first operation
* Run the plugin
* On the settings tab, enter the URL, Username and Password provided by Astun Technology.
* Continue with the Operation

## Operation ##
* Run the plugin
* On the main tab, select the template you wish to export.
* Either enter the destination directory manually in the textbox or click on the `...` button to browse for a directory.
* Click OK
* As long as everything goes as expected, you will end up with an HTML file in the destination directory called similar to the template title.
