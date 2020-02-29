# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Numerical digitize - sets up a Qgis actions for append and edit features
 by inserting or changing numerical values of vertex's coordinates
 A QGIS plugin
                              -------------------
        begin                : 2010 year
        git sha              : $Format:%H$
        copyright (C) 2010 Cédric Möri, with stuff from Stefan Ziegler
                      2019 Igor Chumichev
        email                : desertwolf@inbox.ru
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

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QUrl
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QMessageBox, QAction
from qgis.core import (QgsWkbTypes, QgsGeometry, QgsFeature, QgsMapLayer, QgsPoint,
                       QgsMultiPoint, QgsMultiLineString, QgsLineString, QgsMultiPolygon,
                       QgsPolygon, QgsPointXY, QgsApplication, QgsFeatureRequest, QgsVectorLayerUtils)

# initialize Qt resources from file resources.py
from .resources import *
from .addFeatureGUI import AddFeatureGUI
from .chooseFeatureGUI import ChooseFeatureGUI
from .featureFinderTool import FeatureFinderTool
from .reprojectCoordinates import ReprojectCoordinates
import os.path
import webbrowser

#  NumericalDigitize main class for the plugin


class NumericalDigitize:

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

        # Save reference to the QGIS interface
        self.iface = iface

        # Initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            "i18n",
            "numericalDigitize_{}.qm".format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        # Action button, only one for this version
        self.actions = []
        self.menu = self.translate_str("&Numerical Digitize")

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        self.first_start_edit = None

        # Coordinate system for used coordinates
        self.crsId = None

        # Map Canvas reference
        self.canvas = self.iface.mapCanvas()
        self.EditFeatureMapTool = None
        self.prevMapTool = None

        # Main dialog's references
        self.__dlg = None
        self.__dlgEdit = None
        self.__dlgChooser = None

        # Current layer and it't parameters
        self.__layer = None
        self.__layergeometryType = None
        self.__layerwkbType = None
        self.__hasZ = False
        self.__hasM = False
        self.__isMultiType = False
        self.__isEditMode = False

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon = QIcon(self.plugin_dir + "/images/icon.svg")
        action = QAction(icon, self.translate_str("Numerical digitize"), self.iface.mainWindow())
        action.triggered.connect(self.run)
        action.setEnabled(False)
        action.setWhatsThis(self.translate_str("Numerical digitizing"))
        self.iface.digitizeToolBar().addAction(action)
        self.iface.addPluginToVectorMenu(self.menu, action)
        self.actions.append(action)

        icon = QIcon(self.plugin_dir + "/images/icon-edit.svg")
        action = QAction(icon, self.translate_str("Numerical edit"), self.iface.mainWindow())
        action.triggered.connect(self.runEdit)
        action.setEnabled(False)
        action.setWhatsThis(self.translate_str("Numerical edit"))
        self.iface.digitizeToolBar().addAction(action)
        self.iface.addPluginToVectorMenu(self.menu, action)
        self.actions.append(action)

        # Help
        icon = QIcon(self.plugin_dir + '/images/mActionHelpContents.svg')
        action = QAction(icon, self.translate_str("Help"), self.iface.mainWindow())
        action.triggered.connect(self.help)
        self.iface.addPluginToVectorMenu(self.menu, action)
        self.actions.append(action)

        # will be set False in run()
        self.first_start = True
        self.first_start_edit = True

        # Connect to signals for button behaveour
        self.canvas.currentLayerChanged.connect(self.toggle)
        self.canvas.mapToolSet.connect(self.deactivate)

        # Set action button state for current layer
        self.toggle()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(self.translate_str("&Numerical Digitize"), action)
            self.iface.digitizeToolBar().removeAction(action)
        try:
            self.canvas.currentLayerChanged.disconnect(self.toggle)
        except Exception:
            pass
        try:
            self.canvas.mapToolSet.disconnect(self.deactivate)
        except Exception:
            pass

    # Internal translation function. Noinspection PyMethodMayBeStatic
    @staticmethod
    def translate_str(message):
        """Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        :param message: String for translation.
        :type message: str, QString
        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('NumericalDigitize', message)

    def __setlayerproperties(self):
        self.__layergeometryType = self.__layer.geometryType()
        self.__layerwkbType = self.__layer.wkbType()
        self.__hasZ = QgsWkbTypes.hasZ(self.__layerwkbType)
        self.__hasM = QgsWkbTypes.hasM(self.__layerwkbType)
        self.__isMultiType = QgsWkbTypes.isMultiType(self.__layerwkbType)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start:
            self.first_start = False
            self.__dlg = AddFeatureGUI(self.iface.mainWindow())
            self.__dlg.returnCoordList.connect(self.createGeom)
            self.__dlg.selectedCRS.connect(self.doTransformFromCrs)
            self.__dlg.configureSignals()
            self.__dlg.setWindowTitle(self.translate_str('Add feature'))

        self.__setlayerproperties()
        self.__isEditMode = False
        # noinspection PyArgumentList
        self.__dlg.clearControls()
        self.__dlg.configureDialog(self.__layergeometryType, self.__layerwkbType, self.__isMultiType,
                                   self.__hasZ, self.__hasM, self.__isEditMode, self.canvas)
        self.__dlg.show()

    def runEdit(self):
        # Run method that performs all the real work
        self.__isEditMode = True
        self.prevMapTool = self.canvas.mapTool()
        self.EditFeatureMapTool = FeatureFinderTool(self.canvas)
        self.EditFeatureMapTool.Clicked.connect(self.EditFeature)
        self.canvas.setMapTool(self.EditFeatureMapTool)

    def help(self):
        # Display html help
        url = QUrl.fromLocalFile(self.plugin_dir + "/help" + self.translate_str("/index_en.html")).toString()
        webbrowser.open(url, new=2)

    def EditFeature(self, Rectangle):
        # Restore cursor and previous map tool
        self.EditFeatureMapTool.Clicked.disconnect(self.EditFeature)
        QgsApplication.restoreOverrideCursor()
        self.iface.mapCanvas().setMapTool(self.prevMapTool)

        layer = self.canvas.currentLayer()
        feature_list = list()

        if layer is not None and Rectangle is not None:
            request = QgsFeatureRequest()
            request.setFilterRect(Rectangle.boundingBox())
            request.setFlags(QgsFeatureRequest.ExactIntersect)
            feature_list = list(layer.getFeatures(request))

            if len(feature_list) == 0:
                QMessageBox.critical(self.iface.mainWindow(),
                                     self.translate_str("Numerical edit error"),
                                     self.translate_str("No feature selected"), QMessageBox.Ok)
                self.feature_id = None
            elif len(feature_list) > 1:
                if self.__dlgChooser is None:
                    self.__dlgChooser = ChooseFeatureGUI(self.iface.mainWindow())
                    self.__dlgChooser.configureSignals()

                self.__dlgChooser.clearControls()
                self.__dlgChooser.configureDialog(feature_list, self.__layer)
                if self.__dlgChooser.exec() == 1:
                    self.feature_id = feature_list[self.__dlgChooser.selectedFeature].id()
                else:
                    self.feature_id = None
            else:
                self.feature_id = feature_list[0].id()

        if self.feature_id is not None:
            Feature = layer.getFeature(self.feature_id)
            coords = list()
            self.__setlayerproperties()

            self.createCoords(coords, Feature)

            if self.first_start_edit:
                self.first_start_edit = False
                self.__dlgEdit = AddFeatureGUI(self.iface.mainWindow())
                self.__dlgEdit.returnCoordList.connect(self.createGeom)
                self.__dlgEdit.selectedCRS.connect(self.doTransformFromCrs)
                self.__dlgEdit.configureSignals()
                self.__dlgEdit.setWindowTitle(self.translate_str('Edit feature'))

            # noinspection PyArgumentList
            self.__dlgEdit.clearControls()
            self.__dlgEdit.configureDialog(self.__layergeometryType, self.__layerwkbType, self.__isMultiType,
                                           self.__hasZ, self.__hasM, self.__isEditMode, self.canvas)
            self.__dlgEdit.setValues(coords)
            self.__dlgEdit.show()

    def createCoords(self, coords, feature):
        """
        :param coords: reference at empty list
        :param feature: reference at QgsFeature
        :return: none
        """
        geom = feature.geometry()
        if self.__layergeometryType == QgsWkbTypes.PointGeometry:
            coords.append(['1', list()])
            if self.__isMultiType:
                for part in geom.constParts():
                    for vertex in part.vertices():
                        row = list([vertex.x(), vertex.y()])
                        if self.__hasZ:
                            row.append(vertex.z())
                        if self.__hasM:
                            row.append(vertex.m())
                        coords[0][1].append(row)
            else:
                for vertex in geom.vertices():
                    row = list([vertex.x(), vertex.y()])
                    if self.__hasZ:
                        row.append(vertex.z())
                    if self.__hasM:
                        row.append(vertex.m())
                    coords[0][1].append(row)

        elif self.__layergeometryType == QgsWkbTypes.LineGeometry:
            if self.__isMultiType:
                part_num = 0
                for part in geom.constParts():
                    coords.append([str(part_num + 1), list()])
                    for vertex in part.vertices():
                        row = list([vertex.x(), vertex.y()])
                        if self.__hasZ:
                            row.append(vertex.z())
                        if self.__hasM:
                            row.append(vertex.m())
                        coords[part_num][1].append(row)
                    part_num = part_num + 1
            else:
                coords.append(['1', list()])
                for vertex in geom.vertices():
                    row = list([vertex.x(), vertex.y()])
                    if self.__hasZ:
                        row.append(vertex.z())
                    if self.__hasM:
                        row.append(vertex.m())
                    coords[0][1].append(row)

        elif self.__layergeometryType == QgsWkbTypes.PolygonGeometry:
            if self.__isMultiType:
                part_num = 0
                ring_num = 0
                for part in geom.constParts():
                    ring = part.exteriorRing()
                    coords.append([str(part_num + 1), list()])
                    for vertex in ring.vertices():
                        row = list([vertex.x(), vertex.y()])
                        if self.__hasZ:
                            row.append(vertex.z())
                        if self.__hasM:
                            row.append(vertex.m())
                        coords[part_num + ring_num][1].append(row)

                    # If first and last point identical - remove last point
                    part_list = coords[part_num + ring_num][1]
                    if part_list[0][0] == part_list[len(part_list) - 1][0] and \
                            part_list[0][1] == part_list[len(part_list) - 1][1]:
                        del part_list[-1]

                    part_num = part_num + 1

                    intrings = part.numInteriorRings()
                    for i in range(intrings):
                        ring = part.interiorRing(i)
                        coords.append([str(-(ring_num + 1)), list()])
                        for vertex in ring.vertices():
                            row = list([vertex.x(), vertex.y()])
                            if self.__hasZ:
                                row.append(vertex.z())
                            if self.__hasM:
                                row.append(vertex.m())
                            coords[part_num + ring_num][1].append(row)

                        # If first and last point identical - remove last point
                        part_list = coords[part_num + ring_num][1]
                        if part_list[0][0] == part_list[len(part_list) - 1][0] and \
                                part_list[0][1] == part_list[len(part_list) - 1][1]:
                            del part_list[-1]

                        ring_num = ring_num + 1

    def toggle(self):
        """ When current layer changed  """
        self.__layer = self.canvas.currentLayer()
        # Decide whether the plugin button/menu is enabled or disabled
        if self.__layer is not None:
            if self.__layer.type() == QgsMapLayer.VectorLayer:
                self.__setlayerproperties()

                if self.__layer.isEditable() and (
                        self.__layergeometryType == QgsWkbTypes.PointGeometry
                        or self.__layergeometryType == QgsWkbTypes.LineGeometry
                        or self.__layergeometryType == QgsWkbTypes.PolygonGeometry):
                    for action in self.actions:
                        action.setEnabled(True)
                    self.__layer.editingStopped.connect(self.toggle)
                    try:
                        self.__layer.editingStarted.disconnect(self.toggle)
                    except Exception:
                        pass
                else:
                    for action in self.actions:
                        if action.text() != self.translate_str("Help"):
                            action.setEnabled(False)
                    self.__layer.editingStarted.connect(self.toggle)
                    try:
                        self.__layer.editingStopped.disconnect(self.toggle)
                    except Exception:
                        pass

    def deactivate(self):
        # Set uncheck the button when selected other tool
        self.actions[0].setChecked(False)

    # noinspection PyPep8Naming
    def doTransformFromCrs(self, crsId):
        self.crsId = crsId

      # noinspection PyPep8Naming
    def createGeom(self, coords):

        crsDest = self.__layer.crs()

        rc = ReprojectCoordinates(self.crsId, crsDest.srsid(), self.__hasZ, self.__hasM)
        if self.crsId != crsDest.srsid():
            coordsPoint = list(rc.reproject(coords, True))
        else:
            coordsPoint = list(rc.copyCoordstoPoints(coords))

        # Point and multipoint Geometry
        # Always 1 part, 0 element of matrix
        if self.__layergeometryType == QgsWkbTypes.PointGeometry:
            if self.__isMultiType:
                multipoint = QgsMultiPoint()
                for coords_item in coordsPoint[0][1]:
                    multipoint.addGeometry(coords_item)

                geom = QgsGeometry(multipoint)
                self.createFeature(geom)
            else:
                geom = QgsGeometry(coordsPoint[0][1][0])
                self.createFeature(geom)

        elif self.__layergeometryType == QgsWkbTypes.LineGeometry:
            if self.__isMultiType:
                multiline = QgsGeometry(QgsMultiLineString())
                for j in range(len(coordsPoint)):
                    line = QgsLineString(coordsPoint[j][1])
                    multiline.addPart(line)
                self.createFeature(multiline)
            else:
                line = QgsGeometry(QgsLineString(coordsPoint[0][1]))
                self.createFeature(line)

        elif self.__layergeometryType == QgsWkbTypes.PolygonGeometry:
            if self.__isMultiType:
                multipoly = QgsGeometry(QgsMultiPolygon())

                for i in range(len(coordsPoint)):
                    if int(coordsPoint[i][0]) > 0:
                        mycurve = QgsLineString(coordsPoint[i][1])
                        poly = QgsPolygon()
                        poly.setExteriorRing(mycurve)

                        polyGeometry = QgsGeometry(QgsPolygon(poly))
                        for j in range(len(coordsPoint)):
                            if int(coordsPoint[j][0]) < 0:
                                containsAllPoints = True
                                for k in range(len(coordsPoint[j][1])):
                                    containsAllPoints = True
                                    curPoint = QgsPoint(coordsPoint[j][1][k])
                                    containsAllPoints = containsAllPoints \
                                                    and polyGeometry.contains(QgsPointXY(curPoint.x(), curPoint.y()))
                                if containsAllPoints:
                                    mycurve = QgsLineString(coordsPoint[j][1])
                                    poly.addInteriorRing(mycurve)

                        multipoly.addPart(poly)
                self.createFeature(multipoly)
            else:
                extRing = 0
                for i in range(len(coordsPoint)):
                    if int(coordsPoint[i][0]) > 0:
                       extRing = i

                mycurve = QgsLineString(coordsPoint[extRing][1])
                poly = QgsPolygon()
                poly.setExteriorRing(mycurve)

                polyGeometry = QgsGeometry(QgsPolygon(poly))

                for i in range(len(coordsPoint)):
                    if int(coordsPoint[i][0]) < 0:
                        containsAllPoints = True
                        for j in range(len(coordsPoint[i][1])):
                            containsAllPoints = True
                            curPoint = QgsPoint(coordsPoint[i][1][j])
                            containsAllPoints = containsAllPoints \
                                                and polyGeometry.contains(QgsPointXY(curPoint.x(), curPoint.y()))
                        if containsAllPoints:
                            mycurve = QgsLineString(coordsPoint[i][1])
                            poly.addInteriorRing(mycurve)
                        else:
                            QMessageBox.question(self.iface.mainWindow(),
                                                 self.translate_str("Ring not in exterior contour"),
                                                 self.translate_str("The new geometry of the feature"
                                                                    " isn't valid. Do you want to use it anyway?"),
                                                 QMessageBox.Yes, QMessageBox.No)

                self.createFeature(QgsGeometry(poly))

    def createFeature(self, geom):
        provider = self.__layer.dataProvider()

        if not self.__isEditMode:
            feature = QgsVectorLayerUtils.createFeature(self.__layer)
        else:
            feature = self.__layer.getFeature(self.feature_id)

        if not (geom.validateGeometry()):
            feature.setGeometry(geom)
        else:
            reply = QMessageBox.question(self.iface.mainWindow(),
                                         self.translate_str("Feature not valid"),
                                         self.translate_str("The new geometry of the feature isn't "
                                                            "valid. Do you want to use it anyway?"),
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                feature.setGeometry(geom)
            else:
                return False

        if not self.__isEditMode:
            self.__layer.beginEditCommand("Feature added")
            if self.iface.openFeatureForm(self.__layer, feature):
                self.__layer.addFeature(feature)
            self.__layer.endEditCommand()
        else:
            self.__layer.beginEditCommand("Feature updated")
            self.__layer.updateFeature(feature)
            self.__layer.endEditCommand()

        self.canvas.refresh()
