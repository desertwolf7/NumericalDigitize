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

from qgis.PyQt.QtWidgets import QTableWidget, QTableWidgetItem
from qgis.PyQt.QtCore import QVariant, QMetaType, QCoreApplication, Qt, QModelIndex
from qgis.PyQt.QtGui import QBrush, QColor
from qgis.core import QgsWkbTypes, QgsError
from qgis.gui import QgsErrorDialog
from enum import Enum
from math import isnan


class CellValue(Enum):
    ValueNone = 0
    ValueNotFloat = 1
    ValueFloat = 2


# Values checker class
class ValueChecker:

    def __init__(self, p_tableViewWidget: QTableWidget, p_geometryType):
        self.tableViewWidget = p_tableViewWidget
        self.geometryType = p_geometryType

    @staticmethod
    def checkValue(value: QVariant):
        if value.isNull():
            return CellValue.ValueNone
        if value.convert(QMetaType.QString):
            if str(value.value()) == "":
                return CellValue.ValueNone
        if value.convert(QMetaType.Float):
            if isnan(float(value.value())):
                return CellValue.ValueNotFloat
            else:
                return CellValue.ValueFloat
        else:
            return CellValue.ValueNotFloat

    def checkCellValue(self, item: QTableWidgetItem):
        if item is None:
            return CellValue.ValueNone

        return self.checkValue(QVariant(item.text()))

    def checkModelValue(self, i, j):
        model = self.tableViewWidget.model()

        if i > model.rowCount() or i < 0:
            return CellValue.ValueNone
        if j > model.columnCount() or j < 0:
            return CellValue.ValueNone

        return self.checkValue(QVariant(model.data(model.index(i, j, QModelIndex()), Qt.EditRole)))

    def isCurrentPartValid(self, highlightErrors=False):
        partValid = True
        model = self.tableViewWidget.model()
        for i in range(model.rowCount() - 1):
            partValid = partValid and self.isRowValid(i, highlightErrors)

        if self.isLastRowEmpty():
            return partValid
        else:
            partValid = partValid and self.isRowValid(model.rowCount() - 1, highlightErrors)
            return partValid

    def isRowValid(self, RowNum, highlightErrors=False):
        RowValid = True
        model = self.tableViewWidget.model()
        if RowNum > model.rowCount() - 1 or RowNum < 0:
            return False

        for i in range(model.columnCount()):
            theValue = self.checkModelValue(RowNum, i)
            RowValid = RowValid and (theValue == CellValue.ValueFloat)

            if highlightErrors and theValue == CellValue.ValueNotFloat:
                self.tableViewWidget.item(RowNum, i).setForeground(QBrush(QColor(255, 0, 0)))

        return RowValid

    # check last row is empty?
    def isLastRowEmpty(self):
        lastRowEmpty = True
        model = self.tableViewWidget.model()
        i = model.rowCount() - 1
        for j in range(model.columnCount()):
            lastRowEmpty = lastRowEmpty and (self.checkModelValue(i, j) == CellValue.ValueNone)

        return lastRowEmpty

    def checkCoordsMatrix(self, coords):
        strResult = QgsError()

        for i in range(len(coords)):
            partNumber = str(coords[i][0])
            listValues = coords[i][1]

            if len(listValues) == 0:
                strResult.append(self.translate_str("Part ") +
                                 str(partNumber) + self.translate_str(" is empty"), self.translate_str("Value error"))
            elif self.geometryType == QgsWkbTypes.LineGeometry and len(listValues) < 2:
                strResult.append(self.translate_str("Part ") + str(partNumber) +
                                 self.translate_str(" contains below 2 points."
                                                    " It's not enough for creating line geometry"),
                                 self.translate_str("Value error"))
            elif self.geometryType == QgsWkbTypes.Polygon and len(listValues) < 3:
                strResult.append(self.translate_str("Part ") + str(partNumber) +
                                 self.translate_str(" contains below 3 points. It's not enough "
                                                    "for creating polygon geometry"), self.translate_str("Value error"))
            else:
                for j in range(len(listValues)):
                    currentTuple = listValues[j]
                    for k in range(len(currentTuple)):
                        cellStatus = self.checkValue(QVariant(currentTuple[k]))
                        if cellStatus == CellValue.ValueNone:
                            strResult.append(self.translate_str("Part ") + str(partNumber) +
                                             self.translate_str(" row ") + str(j + 1) +
                                             self.translate_str(" column ") + str(k + 1) +
                                             self.translate_str(" contains empty value"),
                                             self.translate_str("Value error"))
                        elif cellStatus == CellValue.ValueNotFloat:
                            strResult.append(self.translate_str("Part ") + str(partNumber) +
                                             self.translate_str(" row ") + str(j + 1) +
                                             self.translate_str(" column ") + str(k + 1) +
                                             self.translate_str(" contains incorrect value"),
                                             self.translate_str("Value error"))

        if not strResult.isEmpty():
            errorDialog = QgsErrorDialog(strResult,
                                         self.translate_str('Values errors found'),
                                         self.tableViewWidget.parent())
            errorDialog.showNormal()
            return False
        else:
            return True

    def setOkButtonState(self):
        
        # Enable OK button when:
        # If layertype - point and entered point => 1
        # If layertype - polyline and entered point => 2
        # If layertype - polygone and entered point => 3
        
        if self.geometryType == QgsWkbTypes.PointGeometry and (self.tableViewWidget.rowCount()) >= 1:
            return True
        elif self.geometryType == QgsWkbTypes.LineGeometry and (self.tableViewWidget.rowCount()-1) >= 2:
            return True
        elif self.geometryType == QgsWkbTypes.PolygonGeometry and (self.tableViewWidget.rowCount()-1) >= 3:
            return True
        else:
            return False

    @staticmethod
    def translate_str(message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("ValueChecker", message)
