# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Numerical digitize - sets up a Qgis actions for append and edit features
 by inserting or changing digital values of vertex's coordinates
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

from qgis.PyQt.QtCore import Qt, QVariant, QMetaType
from qgis.core import (QgsCoordinateReferenceSystem, QgsWkbTypes, QgsCoordinateTransform, QgsProject, QgsPointXY,
                       QgsPoint, QgsRectangle)
from qgis.gui import QgsRubberBand
from math import isnan


class HighlightFeature:

    def __init__(self, canvas, p_pointsonly, p_closecontour, projectcrs_id):
        self.canvas = canvas

        # Highliting conturs and nodes
        self.lineHighlight = None
        self.nodesHighlight = list()
        self.projectCrsId = projectcrs_id
        self.featureCrsId = -1
        self.pointsOnly = p_pointsonly
        self.closeContour = p_closecontour

    def createHighlight(self, coords, featurecrs_id, currentVertex=0):
        """
        coords - list of tuples with coordinates
        """
        needTransformation = False
        self.featureCrsId = featurecrs_id
        if self.featureCrsId != self.projectCrsId:
            needTransformation = True
            crsSrc = QgsCoordinateReferenceSystem(self.featureCrsId, QgsCoordinateReferenceSystem.InternalCrsId)
            crsDest = QgsCoordinateReferenceSystem(self.projectCrsId, QgsCoordinateReferenceSystem.InternalCrsId)
            transformation = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance())

        if not self.pointsOnly:
            self.lineHighlight = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
            for i in range(len(coords)):
                if self.isFloat(coords[i][0]) and self.isFloat(coords[i][1]):
                    if needTransformation:
                        src_point = QgsPoint(float(coords[i][0]), float(coords[i][1]))
                        src_point.transform(transformation)
                        point = QgsPointXY(src_point)
                    else:
                        point = QgsPointXY(float(coords[i][0]), float(coords[i][1]))
                    self.lineHighlight.addPoint(point, True, 0)

            if self.closeContour and self.lineHighlight.numberOfVertices() > 2:
                self.lineHighlight.closePoints(True)

            self.lineHighlight.setColor(Qt.red)
            self.lineHighlight.setWidth(2)

        j = 0
        for i in range(len(coords)):
            if self.isFloat(coords[i][0]) and self.isFloat(coords[i][1]):
                self.nodesHighlight.append(QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry))
                if needTransformation:
                    src_point = QgsPoint(float(coords[i][0]), float(coords[i][1]))
                    src_point.transform(transformation)
                    point = QgsPointXY(src_point)
                else:
                    point = QgsPointXY(float(coords[i][0]), float(coords[i][1]))
                self.nodesHighlight[j].addPoint(point, True, 0)

                if i == currentVertex:
                    self.nodesHighlight[j].setIcon(QgsRubberBand.ICON_FULL_BOX)
                    self.nodesHighlight[j].setColor(Qt.darkRed)
                else:
                    self.nodesHighlight[j].setIcon(QgsRubberBand.ICON_FULL_DIAMOND)
                    self.nodesHighlight[j].setColor(Qt.darkBlue)
                self.nodesHighlight[j].setIconSize(10)
                j = j + 1

        if len(self.nodesHighlight) > 0:
            x_list = list()
            y_list = list()
            for i in range(len(self.nodesHighlight)):
                x_list.append(self.nodesHighlight[i].getPoint(0).x())
                y_list.append(self.nodesHighlight[i].getPoint(0).y())

            featureRect = QgsRectangle(min(x_list), min(y_list), max(x_list), max(y_list))
            mapRect = self.canvas.extent()
            if not mapRect.contains(featureRect):
                self.canvas.setExtent(featureRect)

        self.canvas.refresh()

    def changeCurrentVertex(self, currentVertex=0):
        if self.nodesHighlight is not None:
            for i in range(len(self.nodesHighlight)):
                if i == currentVertex:
                    self.nodesHighlight[i].setIcon(QgsRubberBand.ICON_FULL_BOX)
                    self.nodesHighlight[i].setColor(Qt.darkRed)
                else:
                    self.nodesHighlight[i].setIcon(QgsRubberBand.ICON_FULL_DIAMOND)
                    self.nodesHighlight[i].setColor(Qt.darkBlue)

        self.canvas.refresh()

    def removeHighlight(self):
        if self.lineHighlight is not None:
            self.canvas.scene().removeItem(self.lineHighlight)
            self.lineHighlight.reset(QgsWkbTypes.LineGeometry)
            self.lineHighlight = None

        for i in range(len(self.nodesHighlight)):
            self.canvas.scene().removeItem(self.nodesHighlight[i])
            self.nodesHighlight[i].reset(QgsWkbTypes.PointGeometry)
        self.nodesHighlight.clear()

        self.canvas.refresh()

    @staticmethod
    def isFloat(value):
        q_value = QVariant(value)

        if q_value.isNull():
            return False
        if q_value.convert(QMetaType.QString):
            if str(q_value.value()) == '':
                return False
        if q_value.convert(QMetaType.Float):
            if isnan(float(q_value.value())):
                return False
            else:
                return True
        else:
            return False
