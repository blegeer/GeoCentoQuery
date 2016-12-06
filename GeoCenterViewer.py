# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoCentoViewer
                                 A QGIS plugin
 Query GeoCento sources and view metadata
                              -------------------
        begin                : 2016-11-16
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Beau Legeer
        email                : beau.legeer@digitalglobe.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QDate, QUrl
from PyQt4.QtGui import QAction, QIcon, QTableWidgetItem, QAbstractItemView, QMessageBox, QCalendarWidget
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from GeoCenterViewer_dialog import GeoCentoViewerDialog
import os.path
import json
import urllib
import urllib2
from qgis.core import *


class GeoCentoViewer:
	"""QGIS Plugin Implementation."""

	def __init__(self, iface):
		"""Constructor.

		:param iface: An interface instance that will be passed to this class
			which provides the hook by which you can manipulate the QGIS
			application at run time.
		:type iface: QgsInterface
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
			'GeoCentoViewer_{}.qm'.format(locale))
			
		if os.path.exists(locale_path):
			self.translator = QTranslator()
			self.translator.load(locale_path)
			
			if qVersion() > '4.3.3':
				QCoreApplication.installTranslator(self.translator)
				

		# Declare instance attributes
		self.actions = []
		self.menu = self.tr(u'&GeoCento Viewer')
		# TODO: We are going to let the user set this up in a future iteration
		self.toolbar = self.iface.addToolBar(u'GeoCentoViewer')
		self.toolbar.setObjectName(u'GeoCentoViewer')
		
		# self.iface.mapCanvas().extentsChanged.connect(self.mapExtentsChanged)
		
		
		
		
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
		return QCoreApplication.translate('GeoCentoViewer', message)


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
		self.dlg = GeoCentoViewerDialog()

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

		icon_path = ':/plugins/GeoCentoViewer/icon.png'
		self.add_action(
			icon_path,
			text=self.tr(u'Query GeoCento Service'),
			callback=self.run,
			parent=self.iface.mainWindow())


	def unload(self):
		"""Removes the plugin menu item and icon from QGIS GUI."""
		for action in self.actions:
			self.iface.removePluginMenu(
				self.tr(u'&GeoCento Viewer'),
				action)
			self.iface.removeToolBarIcon(action)
		
		# remove the toolbar
		del self.toolbar


	def run(self):
		"""Run method that performs all the real work"""
		
		# show the dialog
		self.dlg.show()
		
		sCalPopup = QCalendarWidget()
		eCalPopup = QCalendarWidget()
		self.dlg.startDate.setCalendarPopup(True)
		self.dlg.startDate.setCalendarWidget(sCalPopup)
		self.dlg.endDate.setCalendarPopup(True)
		self.dlg.endDate.setCalendarWidget(eCalPopup)
		
		
		self.dlg.startDate.setDate(	QDate(2016,11,11))
		self.dlg.endDate.setDate(QDate(2016,11,18))
		
		self.dlg.queryTable.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.dlg.queryTable.setHorizontalHeaderLabels(['providername', 
			'type',
			'satellitename',
			'instrumentname',
			'sensortype',
			'sensorband',
			'sensorresolution', 
			'date',
			'cloudcover',
			'price'])
		self.mapExtentsChanged()
		self.iface.mapCanvas().extentsChanged.connect(self.mapExtentsChanged)
		self.dlg.queryButton.clicked.connect(self.mapExtentsChanged)
		self.dlg.queryTable.cellClicked.connect(self.tableClicked)
			
		# Run the dialog event loop
		result = self.dlg.exec_()
		# See if OK was pressed
		if result:
			# Do something useful here - delete the line containing pass and
			# substitute with your code.
			print("Goodbye")
		
	def tableClicked(self, item1, item2):
	
		# print item1, item2
		print("Selection: "+str(item1)+' '+str(item2))
		selected = self.json["products"][item1]
		
		coords = selected["coordinatesWKT"]
		gem = QgsGeometry.fromWkt(coords)
		layer =  QgsVectorLayer('Polygon?crs=epsg:4326', selected["satelliteName"]+":"+selected["productId"] , "memory")
		pr = layer.dataProvider() 
		poly=QgsFeature()
		poly.setGeometry(gem)
		layer.setLayerTransparency(40)
		
		pr.addFeatures([poly])
		layer.updateExtents()
		QgsMapLayerRegistry.instance().addMapLayers([layer])
		
		# print "Thumbnail "+selected["thumbnail"]
		
		# print "QL: "+selected["ql"]
		# overlayLayer = QgsRasterLayer(selected["ql"], selected["productId"], "wms")
		# overlayLayer.isValid()
		# QgsMapLayerRegistry.instance().addMapLayer(overlayLayer)
		
		
			
	def mapExtentsChanged(self):
		# QMessageBox.information( self.iface.mapCanvas(), "Extents changed", "Extents changed" )
		res = self.queryGeoCento()
		if (res is not None):
			self.setTable(res)
		
			
	def queryGeoCento(self):
		
		# get the api Key from the UI
		apiKey = self.dlg.textApiKey.text()
		
		if (not apiKey):
			print("API KEY is not provided")
			return None
		
		#if (self.iface.mapCanvas().currentLayer().crs().srsid() != 4326):
		#	print("WARNING CRS is not geographic - setting to geographic")
		#	self.iface.mapCanvas().currentLayer().setCrs(QgsCoordinateReferenceSystem(4326, True))
			
		urlBase = 'https://earthimages.geocento.com'
		apiEndpoint = '/api/search'
		headers = {'Authorization':'Token '+str(apiKey), 'Content-Type':'application/json'}
		print(headers)
		minRes = self.dlg.resMinSpinner.value()
		maxRes = self.dlg.resMaxSpinner.value()
		aoiWkt = 'POLYGON((40 40, 20 45, 45 30, 40 40))'
		# this must be in geo - convert?
		aoiWkt = self.iface.mapCanvas().extent().asWktPolygon()
		
		self.dlg.statusText.setText("Querying: "+aoiWkt)
		
		#dstart = 1434672000
		dstart = self.dlg.startDate.dateTime().toTime_t()
		#dstop = 1440972000
		dstop = self.dlg.endDate.dateTime().toTime_t()
		

		queryHash = {'sensorFilters':{'maxResolution':maxRes, 'minResolution': minRes}, 
			'aoiWKT':aoiWkt,  
			'start':dstart, 
			'stop':dstop}
	
		
		
		queryData = json.dumps(queryHash)
		print(queryData)
		
		url=urlBase+apiEndpoint
		print (url)
		data = urllib.urlencode(queryHash)

		req = urllib2.Request(url,queryData, headers)
		response = urllib2.urlopen(req)
		the_page = response.read()
		rJson  = json.loads(the_page)
		
		self.json = rJson
		self.dlg.statusText.setText("Ready")
		
		return(rJson)
		
	def ymd2unixtime(s):
		import time
		import datetime
		return(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))
		
	def setTable(self,json):
		'''
		['providername', 
			'type',
			'satellitename',
			'instrumentname',
			'sensortype',
			'sensorband',
			'sensorresolution', 
			'date',
			'cloudcover',
			'price']
		'''
			
		nProducts = len(json["products"])
		rowNum=0
		for p in json["products"]:
			self.dlg.queryTable.setItem(rowNum, 0, QTableWidgetItem(p["providerName"]))
			self.dlg.queryTable.setItem(rowNum, 1, QTableWidgetItem(p["type"]))
			self.dlg.queryTable.setItem(rowNum, 2, QTableWidgetItem(p["satelliteName"]))
			self.dlg.queryTable.setItem(rowNum, 3, QTableWidgetItem(p["instrumentName"]))
			self.dlg.queryTable.setItem(rowNum, 4, QTableWidgetItem(p["sensorType"]))
			self.dlg.queryTable.setItem(rowNum, 5, QTableWidgetItem(p["sensorBand"]))
			self.dlg.queryTable.setItem(rowNum, 6, QTableWidgetItem(str(p["sensorResolution"])))
			self.dlg.queryTable.setItem(rowNum, 7, QTableWidgetItem(str(p["start"])))
			self.dlg.queryTable.setItem(rowNum, 8, QTableWidgetItem(str(p["aoiCoveragePercent"])))
			self.dlg.queryTable.setItem(rowNum, 9, QTableWidgetItem(str(p["selectionPrice"])))
			rowNum=rowNum+1

			