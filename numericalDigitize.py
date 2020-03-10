# -*- coding: latin1 -*-
#---------------------------------------------------------------------
# 
# Trace Digitize Action - Sets up a Qgis action with/for the vertex tracer tool
#
# Copyright (C) 2010  Cédric Möri, with stuff from Stefan Ziegler
#
# EMAIL: cmoe (at) geoing (dot) ch
# WEB  : www.geoing.ch
#
#---------------------------------------------------------------------
# 
# licensed under the terms of GNU GPL 2
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# 
#---------------------------------------------------------------------
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

# initialize Qt resources from file resources.py
import resources

from nd_addfeaturegui import NdAddFeatureGui


# Our main class for the plugin
class NumericalDigitize:
  
  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface
    self.canvas = self.iface.mapCanvas()
    
      
  def initGui(self):
    # For i18n support
    userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/NumericalDigitize"
    systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/NumericalDigitize"

    overrideLocale = bool(QSettings().value("locale/overrideFlag", False, bool))
    if not overrideLocale:
      localeFullName = QLocale.system().name()[:2]
    else:
      localeFullName = QSettings().value("locale/userLocale", "")

    if QFileInfo(userPluginPath).exists():
      translationPath = userPluginPath + "/i18n/NumericalDigitize_" + localeFullName + ".qm"
    else:
      translationPath = systemPluginPath + "/i18n/NumericalDigitize_" + localeFullName + ".qm"
    
    self.localePath = translationPath
    if QFileInfo(self.localePath).exists():
      self.translator = QTranslator()
      self.translator.load(self.localePath)
      QCoreApplication.installTranslator(self.translator)

    mc = self.canvas
    layer = mc.currentLayer()
    
    # Create action that will start plugin configuration
    self.action = QAction(QIcon(":/plugins/NumericalDigitize/vector-create-keyboard.png"), "Numerical Digitize", self.iface.mainWindow())
    self.action.setEnabled(False)

    
    #Connect to signals for button behaviour
    QObject.connect(self.action, SIGNAL("triggered()"), self.run)
    QObject.connect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer*)"), self.toggle)
    QObject.connect(mc, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)
    
    # Add toolbar button 
    self.iface.digitizeToolBar().addAction(self.action)

    self.doTransformMapToLayer = False
    self.doTransformCrsIdToLayer = False
    
  def unload(self):
    self.iface.digitizeToolBar().removeAction(self.action)
    
    
    
  def toggle(self):
    mc = self.canvas
    layer = mc.currentLayer()
    
    #Decide whether the plugin button/menu is enabled or disabled
    if layer <> None:
      if layer.isEditable() and (layer.geometryType() == 0 or layer.geometryType() == 1 or layer.geometryType() == 2):
        self.action.setEnabled(True)
        QObject.connect(layer,SIGNAL("editingStopped()"),self.toggle)
        QObject.disconnect(layer,SIGNAL("editingStarted()"),self.toggle)
    
      else:
        self.action.setEnabled(False)
        QObject.connect(layer,SIGNAL("editingStarted()"),self.toggle)
        QObject.disconnect(layer,SIGNAL("editingStopped()"),self.toggle)        
                
                
                
  def deactivate(self):
    #uncheck the button/menu and get rid off the VTTool signal
    self.action.setChecked(False)
   
    
    
  def run(self):
    #Here we go...
    mc = self.canvas
    layer = mc.currentLayer()
    
    if layer.isEditable() :
      d = NdAddFeatureGui(self.iface.mainWindow(), layer.geometryType())
      QObject.connect(d,SIGNAL("numericalFeature(PyQt_PyObject)"),self.createGeom)
      QObject.connect(d, SIGNAL("transformOTF_CRS(PyQt_PyObject)"), self.doTransfromOfCoords)
      QObject.connect(d, SIGNAL("transformFromCrs(long)"), self.doTransformFromCrs)
      d.show()
    
    
  def doTransfromOfCoords(self, doTransformMapToLayer):
    #True: use Project CRS, False: use Layer CRS
    self.doTransformMapToLayer = doTransformMapToLayer
    self.doTransformToCrsId = False
  
  def doTransformFromCrs(self, crsId):
    self.doTransformMapToLayer = False
    self.doTransformCrsIdToLayer = True
    self.crsId = crsId
  
  def createGeom(self, coords):
    mc = self.canvas
    layer = mc.currentLayer()

    #the code that was formerly here is obsolet. mapToLayerCoordinates is clever
    #enough to shortcut/decide itself if a transformation is necessary.
    
    if self.doTransformMapToLayer:
        coords_tmp = coords[:]
        coords = []
        for point in coords_tmp:
            transformedPoint = self.canvas.mapRenderer().mapToLayerCoordinates( layer, point )
            coords.append(transformedPoint)

    if self.doTransformCrsIdToLayer:
        coords_tmp = coords[:]
        coords = []
        for point in coords_tmp:
            crsSrc = QgsCoordinateReferenceSystem(self.crsId, QgsCoordinateReferenceSystem.InternalCrsId)
            crsDest = layer.crs()
            xform = QgsCoordinateTransform(crsSrc, crsDest)
            transformedPoint = xform.transform( point )
            coords.append(transformedPoint)
                
    if(layer.geometryType() == 1):
      if(len(coords)>=2):
        g = QgsGeometry().fromPolyline(coords)
        self.createFeature(g)
      else:
        QMessageBox.critical(self.iface.mainWindow(),"Error creating feature", "Invalid geometry for geometry type line")
    elif(layer.geometryType()==2):
      if(len(coords)>=3):
        if not(coords[-1] == coords[0]):
          coords.append(coords[0])
        g = QgsGeometry().fromPolygon([coords])
        self.createFeature(g)
      else:
        QMessageBox.critical(self.iface.mainWindow(),"Error creating feature", "Invalid geometry for geometry type polygon")
    else:
      for i in coords:
        g = QgsGeometry.fromPoint(i)
        self.createFeature(g)

 
 
  def createFeature(self, geom):
    layer = self.canvas.currentLayer() 
    provider = layer.dataProvider()
    f = QgsFeature()
    
    if not(geom.validateGeometry()):
      f.setGeometry(geom)
    else:
      reply = QMessageBox.question(self.iface.mainWindow(), 'Feature not valid',
     "The geometry of the feature you just added isn't valid. Do you want to use it anyway?",
     QMessageBox.Yes, QMessageBox.No)
      if reply == QMessageBox.Yes:
        f.setGeometry(geom)
      else:
        return False
        
    fields = layer.pendingFields()

    try: #API-Break 1.8 vs. 2.0 handling
    	attr = f.initAttributes(len(fields))
    	for i in range(len(fields)):
    		f.setAttribute(i,  provider.defaultValue(i))
      	
    except AttributeError: #<=1.8
      ## Add attributefields to feature.
      for i in fields:
        f.addAttribute(i,  provider.defaultValue(i))
           
    layer.beginEditCommand("Feature added")
    
    #layer.addFeature(f)
    attrDialog = QgsAttributeDialog(layer, f, False)
    attrDialog.setIsAddDialog(True)
    result = attrDialog.exec_()
        
    layer.endEditCommand()
    
    self.canvas.refresh()

