# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IShareGISPrintTemplateExport
                                 A QGIS plugin
 Exports a QGIS Print Composer template to iShareGIS
                              -------------------
        begin                : 2018-03-23
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Astun Technology
        email                : qgisdev@astuntechnology.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtCore import QUrl, QByteArray
from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
import resources
# Import any QGIS resources
from qgis.core import QgsProject, QgsNetworkAccessManager, QgsMessageLog
from qgis.gui import QgsMessageBar
from PyQt4.QtNetwork import QNetworkRequest, QNetworkReply
# Import the code for the dialog
from qgis_print_composer_converter_dialog import IShareGISPrintTemplateExportDialog

import os.path, unicodedata, re, base64

class IShareGISPrintTemplateExport:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'IShareGISPrintTemplateExport_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&iShareGIS Print Template Export')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'IShareGISPrintTemplateExport')
        self.toolbar.setObjectName(u'IShareGISPrintTemplateExport')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('IShareGISPrintTemplateExport', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = IShareGISPrintTemplateExportDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/IShareGISPrintTemplateExport/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'iShareGIS Print Template Export'),
            callback=self.run,
            parent=self.iface.mainWindow())


        # attach the click event to the browse button
        self.dlg.btnSaveDirectoryBrowse.clicked.connect(self.select_save_directory)

        # set the inital values from the settings object
        s = QSettings()
        self.dlg.txtAstunServicesURL.setText(s.value('iShareGISPrintTemplateExporter/AstunServicesUrl'))
        self.dlg.txtSaveDirectory.setText(s.value('iShareGISPrintTemplateExporter/SaveDirectory'))
        self.dlg.txtAstunServicesUsername.setText(s.value('iShareGISPrintTemplateExporter/Username'))
        self.dlg.txtAstunServicesPassword.setText(s.value('iShareGISPrintTemplateExporter/Password'))

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&iShareGIS Print Template Export'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def populateComposerList(self, w):
        w.clear()
        for cView in self.iface.activeComposers():
            w.addItem(cView.composerWindow().windowTitle())

    def get_templates(self, w):
        if len(self.iface.activeComposers()) == 0:
            self.show_message(u'There are currently no print composers in the project'\
                'Please create at least one before running this plugin.')
            self.dlg.close()
        else:
            self.populateComposerList(w)

    def send_request(self, url, template, directory, payload):
        """Sends the request to the server"""
        self.add_log_entry("URL: '{0}'".format(url))
        self.add_log_entry("Template: '{0}'".format(template))
        self.add_log_entry("Directory: '{0}'".format(directory))

        def request_finished(reply):
            networkAccessManager = QgsNetworkAccessManager.instance()
            networkAccessManager.finished.disconnect(request_finished)
            sc = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            if sc == 200:
                ba = reply.readAll()
                bas = str(ba.data())
                path = os.path.join(directory, '{0}.html'.format(self.create_filename(template)))
                try:
                    with open(path, 'w') as f:
                        f.write(bas)
                    self.show_message("Template successfully converted")
                except IOError as e:
                    self.add_log_entry("Error saving template\r\n{0}".format(e), level=QgsMessageLog.CRITICAL)
                    self.show_message("Unable to save template to selected directory", level=QgsMessageBar.CRITICAL)
            else:
                self.add_log_entry("An error occurred while converting the template: {0}".format(sc), level=QgsMessageLog.CRITICAL)
                self.show_message('An error occurred while converting the template', level=QgsMessageBar.CRITICAL)
            reply.deleteLater()

        username = self.dlg.txtAstunServicesUsername.text()
        password = self.dlg.txtAstunServicesPassword.text()

        concatenated = '{0}:{1}'.format(username, password)
        data = base64.encodestring(concatenated).replace('\n','')
        headerData = 'Basic {0}'.format(data)

        req = QNetworkRequest(QUrl(url))
        req.setHeader(QNetworkRequest.ContentTypeHeader, 'application/xml')
        req.setRawHeader(QByteArray('x-template-name'), QByteArray(template))
        req.setRawHeader("Authorization", headerData)
        networkAccessManager = QgsNetworkAccessManager.instance()
        networkAccessManager.finished.connect(request_finished)
        data = QByteArray(payload)
        reply = networkAccessManager.post(req, data)

    # Open Folder Dialog
    # https://stackoverflow.com/questions/3941917/can-the-open-file-dialog-be-used-to-select-a-folder

    def add_log_entry(self, message, level=QgsMessageLog.INFO):
        """Adds a log entry to the QGIS log"""
        QgsMessageLog.logMessage(message, "iShareGIS Template Export", level=level)

    def show_message(self, message, level=QgsMessageBar.INFO):
        self.iface.messageBar().pushMessage(
            'iShareGIS Template Exporter : ',
            self.tr(message),
            level = level,
            duration=5
        )

    # https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    def create_filename(self, value):
        """Creates a safe filename"""
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
        value = unicode(re.sub('[-\s]+', '-', value))
        return value

    def select_save_directory(self):
        """Displays a folder browser dialog"""
        path = QFileDialog.getExistingDirectory(self.dlg, "Select output directory", "", QFileDialog.ShowDirsOnly)
        self.dlg.txtSaveDirectory.setText(path)

    def run(self):
        """Run method that performs all the real work"""
        # get the list of templates
        self.get_templates(self.dlg.cmbTemplateName)

        # set Main to be the active tab
        self.dlg.tabTabs.setCurrentIndex(0)

        # show the dialog
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result and self.dlg.txtAstunServicesURL.text().strip() == '':
            self.show_message('Astun Services URL has not been set. Please enter it in the settings tab', QgsMessageBar.WARN)
        if result:
            s = QSettings()
            s.setValue("iShareGISPrintTemplateExporter/AstunServicesUrl", self.dlg.txtAstunServicesURL.text())
            s.setValue("iShareGISPrintTemplateExporter/SaveDirectory", self.dlg.txtSaveDirectory.text())
            s.setValue('iShareGISPrintTemplateExporter/Username', self.dlg.txtAstunServicesUsername.text())
            s.setValue('iShareGISPrintTemplateExporter/Password', self.dlg.txtAstunServicesPassword.text())

            path_absolute = QgsProject.instance().fileName()
            project_contents = ''
            with open(path_absolute, 'r') as f:
                project_contents = f.read()

            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            self.send_request(s.value("iShareGISPrintTemplateExporter/AstunServicesUrl"), unicode(self.dlg.cmbTemplateName.currentText()), "d:/test", project_contents)
