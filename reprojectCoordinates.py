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

from qgis.core import (QgsPoint, QgsCoordinateReferenceSystem, QgsCoordinateTransform,
                       QgsProject, QgsWkbTypes, QgsGeometry)


class ReprojectCoordinates:

    def __init__(self, fromCRS_id, toCRS_id, p_hasZ, p_hasM):
        crsSrc = QgsCoordinateReferenceSystem(fromCRS_id, QgsCoordinateReferenceSystem.InternalCrsId)
        crsDest = QgsCoordinateReferenceSystem(toCRS_id, QgsCoordinateReferenceSystem.InternalCrsId)
        self.hasZ = p_hasZ
        self.hasM = p_hasM
        self.transformation = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance())

    def copyCoordstoPoints(self, coords):
        if coords is not None:
            coordsPoint = list()

            for j in range(len(coords)):
                element = [coords[j][0], list()]
                coordsPoint.append(element)

                element = coords[j][1]
                for i in range(len(element)):
                    if not (self.hasZ or self.hasM):
                        NodePoint = QgsPoint(float(element[i][0]),
                                             float(element[i][1]), None, None, QgsWkbTypes.Point)
                    elif self.hasZ and not self.hasM:
                        NodePoint = QgsPoint(float(element[i][0]), float(element[i][1]), float(element[i][2]),
                                             None, QgsWkbTypes.PointZ)
                    elif not self.hasZ and self.hasM:
                        NodePoint = QgsPoint(float(element[i][0]), float(element[i][1]), None,
                                             float(element[i][2]), QgsWkbTypes.PointM)
                    else:
                        NodePoint = QgsPoint(float(element[i][0]), float(element[i][1]), float(element[i][2]),
                                             float(element[i][3]), QgsWkbTypes.PointZM)

                    coordsPoint[j][1].append(NodePoint)

            return coordsPoint

    def copyPointstoCoords(self, coordsPoint):
        if coordsPoint is not None:
            coordsFloat = list()
            for j in range(len(coordsPoint)):
                element = [coordsPoint[j][0], list()]
                coordsFloat.append(element)

                element = coordsPoint[j][1]
                for i in range(len(element)):
                    if not (self.hasZ or self.hasM):
                        f_tuple = [float(element[i].x()), float(element[i].y())]
                    elif self.hasZ and not self.hasM:
                        f_tuple = [float(element[i].x()), float(element[i].y()), float(element[i].z())]
                    elif not self.hasZ and self.hasM:
                        f_tuple = [float(element[i].x()), float(element[i].y()), float(element[i].m())]
                    else:
                        f_tuple = [float(element[i].x()), float(element[i].y()), float(element[i].z()),
                                   float(element[i].m())]

                    coordsFloat[j][1].append(f_tuple)

            return coordsFloat

    def reproject(self, coords, retQgsPoints):
        if coords is not None:
            coordsPoint = list(self.copyCoordstoPoints(coords))

            for j in range(len(coordsPoint)):
                element = coordsPoint[j][1]
                for i in range(len(element)):
                    element[i].transform(self.transformation, QgsCoordinateTransform.ForwardTransform, self.hasZ)

            if retQgsPoints:
                return coordsPoint
            else:
                return list(self.copyPointstoCoords(coordsPoint))

    def reprojectGeometry(self, geom: QgsGeometry) -> QgsGeometry:
        if geom is not None:
            geom.transform(self.transformation, QgsCoordinateTransform.ForwardTransform, self.hasZ)
            return geom
