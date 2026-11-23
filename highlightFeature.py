# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Numerical digitize - sets up a Qgis actions for append and edit features
 by inserting or changing numerical values of vertex's coordinates
 A QGIS plugin
                              -------------------
        begin                : 2019 year
        git sha              : $Format:%H$
        copyright (C) 2019 Igor Chumichev
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

from qgis.PyQt.QtCore import Qt, QVariant
from qgis.core import (Qgis, QgsCoordinateReferenceSystem, QgsWkbTypes, QgsCoordinateTransform, QgsProject, QgsPointXY,
                       QgsPoint, QgsRectangle)
from qgis.gui import QgsRubberBand
from math import isnan
from .valueChecker import STRING_TYPE, FLOAT_TYPE

if hasattr(Qgis, 'RubberBandIconType'):
    ICON_BOX = Qgis.RubberBandIconType.BoxFilled
    ICON_DIAMOND = Qgis.RubberBandIconType.DiamondFilled
else:
    ICON_BOX = QgsRubberBand.ICON_FULL_BOX
    ICON_DIAMOND = QgsRubberBand.ICON_FULL_DIAMOND


class HighlightFeature:

    def __init__(self, canvas, p_pointsonly, p_closecontour, p_projectcrs):
        self.canvas = canvas

        # Highliting all conturs and nodes of current contour
        self.lineHighlight = list()
        self.nodesHighlight = list()
        self.projectCrs = p_projectcrs
        self.featureCrs = -1
        self.pointsOnly = p_pointsonly
        self.closeContour = p_closecontour

    def createHighlight(self, coords, currentPart, p_featurecrs, currentVertex=0):
        """
        coords - list of tuples with coordinates coords matrix type from addFeatureGUI
        """
        needTransformation = False
        self.featureCrs = p_featurecrs
        if self.featureCrs != self.projectCrs:
            needTransformation = True
            transformation = QgsCoordinateTransform(self.featureCrs, self.projectCrs, QgsProject.instance())

        if not self.pointsOnly:
            for partNum in range(len(coords)):
                self.lineHighlight.append(QgsRubberBand(self.canvas, QgsWkbTypes.GeometryType.LineGeometry))
                coordsPart = coords[partNum][1]
                for i in range(len(coordsPart)):
                    if self.isFloat(coordsPart[i][0]) and self.isFloat(coordsPart[i][1]):
                        if needTransformation:
                            src_point = QgsPoint(float(coordsPart[i][0]), float(coordsPart[i][1]))
                            src_point.transform(transformation)
                            point = QgsPointXY(src_point)
                        else:
                            point = QgsPointXY(float(coordsPart[i][0]), float(coordsPart[i][1]))
                        self.lineHighlight[partNum].addPoint(point, True, 0)

                if self.closeContour and self.lineHighlight[partNum].numberOfVertices() > 2:
                    self.lineHighlight[partNum].closePoints(True)

                self.lineHighlight[partNum].setColor(Qt.GlobalColor.red)
                self.lineHighlight[partNum].setWidth(2)

        j = 0
        coordsPart = coords[currentPart][1]
        for i in range(len(coordsPart)):
            if self.isFloat(coordsPart[i][0]) and self.isFloat(coordsPart[i][1]):
                self.nodesHighlight.append(QgsRubberBand(self.canvas, QgsWkbTypes.GeometryType.PointGeometry))
                if needTransformation:
                    src_point = QgsPoint(float(coordsPart[i][0]), float(coordsPart[i][1]))
                    src_point.transform(transformation)
                    point = QgsPointXY(src_point)
                else:
                    point = QgsPointXY(float(coordsPart[i][0]), float(coordsPart[i][1]))
                self.nodesHighlight[j].addPoint(point, True, 0)

                if i == currentVertex:
                    self.nodesHighlight[j].setIcon(ICON_BOX)
                    self.nodesHighlight[j].setColor(Qt.GlobalColor.darkRed)
                else:
                    self.nodesHighlight[j].setIcon(ICON_DIAMOND)
                    self.nodesHighlight[j].setColor(Qt.GlobalColor.darkBlue)
                self.nodesHighlight[j].setIconSize(10)
                j = j + 1

        if len(self.nodesHighlight) > 0:
            x_list = list()
            y_list = list()
            for i in range(len(self.nodesHighlight)):
                x_list.append(self.nodesHighlight[i].getPoint(0).x())
                y_list.append(self.nodesHighlight[i].getPoint(0).y())

            featureRect = QgsRectangle(min(x_list), min(y_list), max(x_list), max(y_list))
            # If canvas not contains entire feature then set canvas center on center of feature
            mapRect = self.canvas.extent()
            if not mapRect.contains(featureRect):
                centerPoint = QgsPointXY(float((min(x_list) + max(x_list)) / 2), float((min(y_list) + max(y_list)) / 2))
                self.canvas.setCenter(centerPoint)

                # If now If canvas not contains entire feature then set canvas extent on feature extent
                mapRect = self.canvas.extent()
                if not mapRect.contains(featureRect):
                    self.canvas.setExtent(featureRect)

        self.canvas.refresh()

    def changeCurrentVertex(self, currentVertex=0):
        if self.nodesHighlight is not None:
            for i in range(len(self.nodesHighlight)):
                if i == currentVertex:
                    self.nodesHighlight[i].setIcon(ICON_BOX)
                    self.nodesHighlight[i].setColor(Qt.GlobalColor.darkRed)
                else:
                    self.nodesHighlight[i].setIcon(ICON_DIAMOND)
                    self.nodesHighlight[i].setColor(Qt.GlobalColor.darkBlue)

            self.canvas.refresh()

    def removeHighlight(self):
        if len(self.lineHighlight) > 0:
            for partNum in range(len(self.lineHighlight)):
                self.canvas.scene().removeItem(self.lineHighlight[partNum])
                self.lineHighlight[partNum].reset(QgsWkbTypes.GeometryType.LineGeometry)
            self.lineHighlight.clear()

        for i in range(len(self.nodesHighlight)):
            self.canvas.scene().removeItem(self.nodesHighlight[i])
            self.nodesHighlight[i].reset(QgsWkbTypes.GeometryType.PointGeometry)
        self.nodesHighlight.clear()

        self.canvas.refresh()

    @staticmethod
    def isFloat(value):
        q_value = QVariant(value)

        if q_value.isNull():
            return False
        if q_value.convert(STRING_TYPE):
            if str(q_value.value()) == '':
                return False
        if q_value.convert(FLOAT_TYPE):
            if isnan(float(q_value.value())):
                return False
            else:
                return True
        else:
            return False
