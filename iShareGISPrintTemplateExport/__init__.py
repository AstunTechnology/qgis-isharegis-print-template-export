# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IShareGISPrintTemplateExport
                                 A QGIS plugin
 Exports a QGIS Print Composer template to iShareGIS
                             -------------------
        begin                : 2018-03-23
        copyright            : (C) 2018 by Astun Technology
        email                : qgisdev@astuntechnology.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load IShareGISPrintTemplateExport class from file IShareGISPrintTemplateExport.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .qgis_print_composer_converter import IShareGISPrintTemplateExport
    return IShareGISPrintTemplateExport(iface)
