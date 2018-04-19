# iShareGIS QGIS Print Composer template exporter #
Author: Astun Technology Ltd.

## Introduction ##
This is a QGIS plugin which is used to convert the selected QGIS Print Composer template to an iShare GIS print template.
## Requirements ##
* QGIS 2 (tested with 2.18.18)
* An Astun Services account

## Installation ##
* Extract the zip file
* Copy the iShareGISPrintTemplateExport directory to the QGIS Python plugin directory
  * (`C:\Users\{username}\.qgis2\python\plugins\` on Windows)

## Set up ##
Setup is initially completed on first operation
* Run the plugin
* On the settings tab, enter the URL, Username and Password provided by Astun Technology.
* Continue with the Operation

## Operation ##
* Run the plugin
* On the main tab, select the template you wish to export.
* Either enter the destination directory manually in the textbox or click on the `...` button to browse for a directory.
* Click OK
* You will end up with an HTML file in the destination directory called similar to the template title.

## Templates ##

### Requirements ###
The template must
* Have a single map element

### Limitations ###
While efforts have been made to ensure that the conversion process should produce an iShare GIS print template that is very similar to the original, the process is automated, and therefore cannot guarantee that the output will be exactly the same.

### Pre-defined label content ###
iShare GIS templates can contain labels that will be populated with pre-defined text at runtime.
* Add a label to the template and move/style appropriately.
* Set the ID of the label to one of the IDs in the table below.

| ID           | Value |
|--------------|-------|
| ishare-user  | Current user and domain |
| ishare-timestamp | Current time (e.g. 2018-03-23 14:37:39) |
| ishare-projection | 	The in-use map projection code (e.g. EPSG:27700) |
| ishare-attribution | 	Copyright taken from the base MapSource |
| ishare-scale | 	Current map scale |
| ishare-centre | 	Central co-ordinates of the current view of the map |
| ishare-centre-x	 | |
| ishare-centre-y	 | |
| ishare-bbox | 	Corner co-ordinates of the current view of the map |
| ishare-min-x	 | |
| ishare-min-y	 | |
| ishare-max-x	 | |
| ishare-max-y	 | |

### Editable labels ###
iShare GIS templates can also contain editable labels. These will appear in the print dialog in the left-hand panel where you can edit the contents.
* Add a label to the template and move/style appropriately.
* In the variables panel
  * Add a ComposerItem variable named ```editable``` and set the value to ```true```.
  * Add a ComposerItem variable named ```field``` and set the value to the name of the field (no spaces, all lower case).
* Set the value of the label to what it's default text should be.
