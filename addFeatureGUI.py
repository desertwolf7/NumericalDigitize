# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Numerical digitize - sets up a Qgis actions for append and edit features
 by inserting or changing digital values of vertex's coordinates
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

from qgis.PyQt.QtCore import (QSettings, QVariant, QPersistentModelIndex, pyqtSignal,
                              QCoreApplication, QModelIndex)
from qgis.PyQt.QtGui import QColor, QBrush, QClipboard
from qgis.PyQt.QtWidgets import QMessageBox, QDialogButtonBox, QHeaderView, QTableWidgetItem, QDialog, QApplication
from qgis.core import QgsCoordinateReferenceSystem, QgsWkbTypes
from qgis.gui import QgsProjectionSelectionDialog

from .resources import *
from .highlightFeature import HighlightFeature
from .reprojectCoordinates import ReprojectCoordinates
from .valueChecker import ValueChecker, CellValue
from .ui_addFeatureGUI import Ui_numericalDigitize_MainDialog

import os
from builtins import int, str
currentPath = os.path.dirname(__file__)


# noinspection PyPep8Naming
class AddFeatureGUI(QDialog, Ui_numericalDigitize_MainDialog):

    returnCoordList = pyqtSignal(list)
    selectedCRS = pyqtSignal(int)

    """Matrix of coordinates
    Format: list of lists
    First list - number of parts. Values - always 1 for non multipart features, except polygons, and multipoints 
                                           1 .. N positive numbers for multipart features
                                           -1 .. -N negative numbers for internal rings in polygons  
    Second lists - coordinates of every part. Format - float. Values (X, Y, Z (optional), M (optional))
    """
    coords_matrix = []

    # Previous part for multipart
    prev_row = 0
    layertype = None
    wkbtype = None
    has_Z = False
    has_M = False
    isMultiType = False
    isEditMode = False
    mapCanvas = None
    highLighter = None
    valueChecker = None

    __ignore_changeCellEvent = False
    __part_changing = False
    __contursCount = 1
    __ringsCount = 0

    def __init__(self, parent=None):
        """Constructor."""
        super(AddFeatureGUI, self).__init__(parent)
        self.setupUi(self)
        self.featureCrsId = None
        self.projectCrsId = None

    def configureSignals(self):
        # When change cell check values and append new rows
        self.twPoints.currentCellChanged.connect(self.onCellChanged)
        self.twPoints.cellChanged.connect(self.onCellValueChanged)
        self.twPoints.cellClicked.connect(self.onCellClicked)

        # When OK pressed collect coords and send it for create feature
        self.buttonBox.accepted.connect(self.onOK)
        self.finished.connect(self.onFinished)

        self.toolButtonCopy.clicked.connect(self.copyButtonClicked)
        self.toolButtonPaste.clicked.connect(self.pasteButtonClicked)
        self.toolButtonSwap.clicked.connect(self.swapButtonClicked)
        self.toolButtonAddRows.clicked.connect(self.addRowsButtonClicked)
        self.toolButtonRemoveRows.clicked.connect(self.removeRowsButtonClicked)

        self.toolButtonAddPart.clicked.connect(self.addPartButtonClicked)
        self.toolButtonAddRing.clicked.connect(self.addRingButtonClicked)
        self.toolButtonRemovePart.clicked.connect(self.removePartButtonClicked)
        self.toolButtonReproject.clicked.connect(self.reprojectCoords)

        self.listParts.currentRowChanged.connect(self.partChanged)

        self.rb_OtherCrs.toggled.connect(self.selectOtherCrs)
        self.rb_ProjectCrs.toggled.connect(self.selectProjectCrs)
        self.rb_LayerCrs.toggled.connect(self.selectLayerCrs)

    def clearControls(self):
        """ Clear coordinates store, list and table controls """
        self.coords_matrix.clear()
        element = [1, list()]
        self.coords_matrix.append(element)

        self.prev_row = 0
        self.__contursCount = 0
        self.__ringsCount = 0

        self.highLighter = None

        model = self.twPoints.model()
        model.removeRows(0, model.rowCount())
        model.insertRows(0, 1)

        model = self.listParts.model()
        model.removeRows(0, model.rowCount())

        self.valueChecker = None

    def configureDialog(self, p_layertype, p_wkbtype, p_Multitype=False, p_Z=False, p_M=False, p_EditMode=False,
                        p_Canvas=None):
        """ Init dialog controls """

        self.layertype = p_layertype
        self.wkbtype = p_wkbtype
        self.has_Z = p_Z
        self.has_M = p_M
        self.isMultiType = p_Multitype
        self.isEditMode = p_EditMode
        self.mapCanvas = p_Canvas
        self.projectCrsId = self.mapCanvas.mapSettings().destinationCrs().srsid()
        self.highLighter = HighlightFeature(self.mapCanvas,
                                            self.layertype == QgsWkbTypes.PointGeometry,
                                            self.layertype == QgsWkbTypes.PolygonGeometry,
                                            self.projectCrsId)
        self.valueChecker = ValueChecker(self.twPoints, self.layertype)

        # Hide working with parts for any point geometry and simple line geometry
        if self.layertype == QgsWkbTypes.PointGeometry or \
                (self.layertype == QgsWkbTypes.LineGeometry and not self.isMultiType):
            self.partButtonsFrame.hide()
            self.partsFrame.hide()
            self.gridMainLayout.setHorizontalSpacing(0)

        # Else activate multipart controls
        else:
            self.partButtonsFrame.show()
            self.partsFrame.show()
            self.gridMainLayout.setHorizontalSpacing(3)

            # Set enabled state Add ring button only for polygons
            self.toolButtonAddRing.setEnabled(self.layertype == QgsWkbTypes.PolygonGeometry)

            # Disable add parts buttons for not multipolygone (only add ring enabled)
            self.toolButtonAddPart.setEnabled(self.isMultiType)

            model = self.listParts.model()
            model.blockSignals(True)
            model.insertRows(0, 1)
            model.setData(model.index(0), '1', QtCore.Qt.EditRole)
            model.blockSignals(False)

            self.__contursCount = 1
            self.prev_row = 0

        if self.has_Z and self.has_M:
            tableColumns = 4
            headerLabels = ['X', 'Y', 'Z', 'M']
        elif self.has_Z != self.has_M:
            tableColumns = 3
            if self.has_Z:
                headerLabels = ['X', 'Y', 'Z']
            else:
                headerLabels = ['X', 'Y', 'M']
        else:
            tableColumns = 2
            headerLabels = ['X', 'Y']

        modelColumns = self.twPoints.model().columnCount()

        if tableColumns > modelColumns:
            self.twPoints.model().insertColumns(2, tableColumns - modelColumns)
        elif tableColumns < modelColumns:
            self.twPoints.model().removeColumns(2, modelColumns - tableColumns)

        for i in range(len(headerLabels)):
            if self.twPoints.horizontalHeaderItem(i) is not None:
                self.twPoints.horizontalHeaderItem(i).setText(headerLabels[i])
            else:
                item = QTableWidgetItem()
                item.setText(headerLabels[i])
                self.twPoints.setHorizontalHeaderItem(i, item)

        # Resize grid. Set column's width equal. Resize the section to fill the available space.
        for i in range(self.twPoints.columnCount()):    
            self.twPoints.setColumnWidth(i, self.twPoints.width()/self.twPoints.columnCount())
            self.twPoints.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        # Disable OK button. Wait for entering valid coordinates
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                
        # Disable choose CRS button while not selected rb_ChooseCrs
        self.l_OtherCrsName.setEnabled(False)

        settings = QSettings()

        rb_checked = settings.value("NumericDigitize/checked", "rb_ProjectCrs", type=str)
        if rb_checked == "rb_ProjectCrs":
            self.rb_ProjectCrs.setChecked(True)
            self.featureCrsId = self.projectCrsId
        elif rb_checked == "rb_otherCrs":
            self.rb_OtherCrs.setChecked(True)
            self.featureCrsId = settings.value("NumericDigitize/featureCrsId", -1, type=int)
            self.__displayAuthid()
        else:
            self.rb_LayerCrs.setChecked(True)
            self.featureCrsId = self.mapCanvas.currentLayer().crs().srsid()

        self.selectedCRS.emit(self.featureCrsId)

    @staticmethod
    def translate_str(message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("AddFeatureGUI", message)

    def highLightFeature(self, partNum, vertexNum=-1):
        if self.highLighter is not None:
            self.highLighter.removeHighlight()
            if -1 < partNum < len(self.coords_matrix):
                self.highLighter.createHighlight(self.coords_matrix[partNum][1], self.featureCrsId)
                if -1 < vertexNum < len(self.coords_matrix[partNum][1]):
                    self.highLighter.changeCurrentVertex(vertexNum)

    def setValues(self, coord_list):
        self.coords_matrix = list(coord_list)

        # Fill part list with values
        model = self.listParts.model()
        model.removeRows(0, model.rowCount())
        model.insertRows(0, len(self.coords_matrix))

        self.__contursCount = len([part for part in self.coords_matrix if int(part[0]) > 0])
        self.__ringsCount = len(self.coords_matrix) - self.__contursCount

        model.blockSignals(True)
        for i in range(len(self.coords_matrix)):
            model.setData(model.createIndex(i, 0), QVariant(self.coords_matrix[i][0]))
        model.blockSignals(False)
        model.dataChanged.emit(model.createIndex(0, 0), model.createIndex(model.rowCount() - 1, 0))

        # Fill table with values
        model = self.twPoints.model()
        model.removeRows(0, model.rowCount())
        if self.layertype == QgsWkbTypes.PointGeometry and not self.isMultiType:
            model.insertRows(0, len(self.coords_matrix[0][1]))
        else:
            model.insertRows(0, len(self.coords_matrix[0][1]) + 1)

        coordslist = self.coords_matrix[0][1]
        model.blockSignals(True)

        for i in range(len(coordslist)):
            for j in range(self.twPoints.columnCount()):
                model.setData(model.createIndex(i, j), QVariant(str(coordslist[i][j])))

        model.blockSignals(False)

        self.__part_changing = True
        model.dataChanged.emit(model.createIndex(0, 0),
                               model.createIndex(model.rowCount()-1, model.columnCount()-1))
        self.__part_changing = False

        self.highLightFeature(0, 0)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.valueChecker.setOkButtonState())

    def selectProjectCrs(self, checked):
        if checked:
            self.featureCrsId = self.projectCrsId
            self.selectedCRS.emit(self.projectCrsId)

    def selectLayerCrs(self, checked):
        if checked:
            self.featureCrsId = self.mapCanvas.currentLayer().crs().srsid()
            self.selectedCRS.emit(self.featureCrsId)

    def selectOtherCrs(self, checked):
        if checked:
            self.l_OtherCrsName.setEnabled(True)
            crsSelector = QgsProjectionSelectionDialog()
            crsSelector.setCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
            if crsSelector.exec():
                self.featureCrsId = crsSelector.crs().srsid()
            self.__displayAuthid()
        else:
            self.l_OtherCrsName.setEnabled(False)

    def __displayAuthid(self):
        if self.featureCrsId == -1:
            self.l_OtherCrsName.setText("[%s]" % self.tr("CRS not selected"))
        else:
            self.l_OtherCrsName.setText(
                '[%s]' % QgsCoordinateReferenceSystem(self.featureCrsId,
                                                      QgsCoordinateReferenceSystem.InternalCrsId).authid()
                )
            self.selectedCRS.emit(self.featureCrsId)

    def reprojectCoords(self):
        self.refreshCoordsMatrix(self.prev_row)

        if self.valueChecker.checkCoordsMatrix(self.coords_matrix):
            srcProj = QgsCoordinateReferenceSystem()
            srcProj.createFromSrsId(self.featureCrsId)

            crsSelectorFrom = QgsProjectionSelectionDialog()
            crsSelectorFrom.setCrs(srcProj)
            crsSelectorFrom.setMessage(self.translate_str("Select source coordinates system"))

            if crsSelectorFrom.exec():
                crsSelectorTo = QgsProjectionSelectionDialog()
                crsSelectorTo.setMessage(self.translate_str("Select destination coordinates system"))

                if crsSelectorTo.exec():
                    rc = ReprojectCoordinates(crsSelectorFrom.crs().srsid(), crsSelectorTo.crs().srsid(),
                                              self.has_Z, self.has_M)
                    self.coords_matrix = list(rc.reproject(self.coords_matrix, False))

                    self.__part_changing = True
                    self.refreshTable(self.prev_row)
                    self.__part_changing = False

                    self.featureCrsId = crsSelectorTo.crs().srsid()
                    if self.featureCrsId == self.mapCanvas.currentLayer().crs().srsid():
                        self.rb_LayerCrs.setChecked(True)
                    elif self.featureCrsId == self.projectCrsId:
                        self.rb_ProjectCrs.setChecked(True)
                    else:
                        self.rb_OtherCrs.blockSignals(True)
                        self.rb_OtherCrs.setChecked(True)
                        self.rb_OtherCrs.blockSignals(False)
                        self.__displayAuthid()

    def onCellClicked(self, newRow, newColumn):
        self.highLightFeature(self.prev_row, newRow)

    def onCellValueChanged(self, newRow, newColumn):
        if newRow == -1 or self.__part_changing:
            return
        else:
            self.refreshCoordsMatrix(self.prev_row)
            self.highLightFeature(self.prev_row, newRow)

    def onCellChanged(self, newRow, newColumn, currentRow, currentColumn):
        # Table's cells editing control
        if self.__ignore_changeCellEvent:
            self.__ignore_changeCellEvent = False
            return

        if currentRow == -1 or currentColumn == -1 or self.__part_changing or self.valueChecker is None:
            return

        if self.highLighter is not None and newRow != -1 and not self.__part_changing:
            self.highLighter.changeCurrentVertex(newRow)

        theCell = self.twPoints.item(currentRow, currentColumn)
        theValue = self.valueChecker.checkCellValue(theCell)

        if theValue == CellValue.ValueFloat:
            if theCell.foreground() == QBrush(QColor(255, 0, 0)):
                theCell.setForeground(QBrush(QColor(0, 0, 0)))

            # only add a new row, if all cells are used, also be sure,
            # that only numerics find their way in the table
            if self.twPoints.rowCount() == currentRow + 1:
                # If all values valid and it's not single point geometry - append new row in table
                if self.valueChecker.isRowValid(currentRow) \
                        and (self.isMultiType or self.layertype != QgsWkbTypes.PointGeometry):
                    self.twPoints.setRowCount(self.twPoints.rowCount())
                    self.twPoints.insertRow(self.twPoints.rowCount())
                    self.__ignore_changeCellEvent = True
                    self.twPoints.setCurrentCell(self.twPoints.rowCount() - 1, 0)
                    self.twPoints.edit(self.twPoints.currentIndex())

                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.valueChecker.setOkButtonState())

        elif theValue == CellValue.ValueNotFloat or theValue == CellValue.ValueNone:
            # If value of cell is not number - set foreground red color
            if theValue == CellValue.ValueNotFloat:
                theCell.setForeground(QBrush(QColor(255, 0, 0)))

    def copyButtonClicked(self):
        model = self.twPoints.model()
        textstring = ''
        if self.valueChecker.isLastRowEmpty():
            droprow = 1
        else:
            droprow = 0

        selectedCells = sorted(self.twPoints.selectionModel().selectedIndexes())

        # If zero or one cell selected - copy entire table to clipboard, else copy entire table
        if len(selectedCells) > 1:
            for i in range(model.rowCount() - droprow):
                currentString = ''
                for j in range(model.columnCount()):
                    modelIndex = model.index(i, j, QModelIndex())
                    if selectedCells.__contains__(modelIndex):
                        currentString = currentString + str(model.data(modelIndex, QtCore.Qt.EditRole)) + "\t"
                if len(currentString) > 0:
                    textstring = textstring + currentString[:-1] + "\n"
        else:
            for i in range(model.rowCount() - droprow):
                for j in range(model.columnCount()):
                    textstring = textstring + \
                                 str(model.data(model.index(i, j, QModelIndex()), QtCore.Qt.EditRole)) + "\t"
                textstring = textstring[:-1] + "\n"

        QApplication.clipboard().setText(textstring, QClipboard.Clipboard)

    def pasteButtonClicked(self):
        model = self.twPoints.model()

        pasteString = QApplication.clipboard().text()
        # Create list of strings with removing empty strings
        rows = pasteString.split("\n")
        rows = [row for row in rows if row.replace("\t", "") != ""]

        numRows = len(rows)
        if numRows <= 0:
            return

        numCols = rows[0].count("\t") + 1
        decimalDivider = self.locale().decimalPoint()
        values = list()

        for row in range(numRows):
            # Set correct decimal point according locale
            if decimalDivider == "." and rows[row].find(",") != -1:
                rows[row] = rows[row].replace(',', '.')
            elif decimalDivider == ',' and rows[row].find(".") != -1:
                rows[row] = rows[row].replace(".", ",")

            columns = rows[row].split("\t")
            # Fill empty columns with '0'
            if model.columnCount() > numCols:
                columns.extend("0" for _ in range(model.columnCount() - numCols))

            values.append(columns)

        selectedRows = sorted(self.twPoints.selectionModel().selectedRows())
        selectedCells = sorted(self.twPoints.selectionModel().selectedIndexes())

        # If selected zero or one cell or selected only ine row (and in this case selected cells > = 2)- append rows
        if len(selectedCells) < 2 or len(selectedRows) == 1:
            # If full selected one row - insert new rows before this row and fill it with values from clipboard
            if len(selectedRows) == 1:
                # Insert the amount of rows we need to accomodate the paste before first selected row
                upperRow = selectedRows[0].row()
                model.insertRows(selectedRows[0].row(), numRows)

            # If full selected rows absent - append row after last exist's row
            else:
                # Insert the amount of rows we need to accomodate the paste and one last empty row
                upperRow = model.rowCount() - 1
                model.insertRows(model.rowCount(), numRows)

            model.blockSignals(True)
            for i in range(len(values)):
                l_tuple = values[i]
                # If count of values in row more then columns in table - ignore it
                columnRange = min(len(l_tuple), model.columnCount())
                for j in range(columnRange):
                    model.setData(model.createIndex(upperRow + i, j), QVariant(l_tuple[j]))
            model.blockSignals(False)

        # Fill with values selected cells
        else:
            model.blockSignals(True)
            i_values = 0
            for i in range(model.rowCount()):
                j_values = 0
                for j in range(model.columnCount()):
                    modelIndex = model.index(i, j, QModelIndex())
                    l_tuple = values[i_values]
                    if selectedCells.__contains__(modelIndex):
                        model.setData(modelIndex, QVariant(l_tuple[j_values]))
                        j_values += 1
                if j_values > 0:
                    i_values += 1
                if i_values > len(values) - 1:
                    break
            model.blockSignals(False)

        self.refreshCoordsMatrix(self.prev_row)

        model.dataChanged.emit(model.index(0, 0, QModelIndex()),
                               model.index(model.rowCount()-1, model.columnCount()-1, QModelIndex()))

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.valueChecker.setOkButtonState())

    def swapButtonClicked(self):
        # When swap button pressed exchange values of X and Y in table control and coordinates store
        model = self.twPoints.model()

        self.__part_changing = True
        for i in range(model.rowCount()):
            index1 = model.index(i, 0, QModelIndex())
            index2 = model.index(i, 1, QModelIndex())
            swapvalue = model.data(index1, QtCore.Qt.EditRole)
            model.setData(index1, model.data(index2, QtCore.Qt.EditRole), QtCore.Qt.EditRole)
            model.setData(index2, swapvalue, QtCore.Qt.EditRole)
        self.__part_changing = False

        for i in range(len(self.coords_matrix)):
            current_list = self.coords_matrix[i][1]
            for j in range(len(current_list)):
                swapvalue = current_list[j][0]
                current_list[j][0] = current_list[j][1]
                current_list[j][1] = swapvalue

        self.highLightFeature(self.prev_row, 0)

    def addRowsButtonClicked(self):
        model = self.twPoints.model()
        selectedRows = sorted(self.twPoints.selectionModel().selectedRows())

        # If rows not selected append row after last row
        if len(selectedRows) == 0:
            if not self.valueChecker.isLastRowEmpty():
                model.insertRows(model.rowCount(), 1)
            currentRow = model.rowCount() - 1
        else:
            # Insert row before first selected row
            model.insertRows(selectedRows[0].row(), 1)
            currentRow = selectedRows[0].row()

        self.__ignore_changeCellEvent = True
        self.twPoints.setCurrentCell(currentRow, 0)
        self.twPoints.edit(self.twPoints.currentIndex())

    def removeRowsButtonClicked(self):
        model = self.twPoints.model()
        selectedRows = self.twPoints.selectionModel().selectedRows()
        if len(selectedRows) == 0:
            title = self.translate_str("Warning")
            message = self.translate_str("Remove all rows?")
            msgBox = QMessageBox.warning(self.window(), title, message, QMessageBox.Ok | QMessageBox.Cancel)
            if msgBox == QMessageBox.Ok:
                model.removeRows(0, model.rowCount())
                model.insertRows(0, 1)
        else:
            indexes = [QPersistentModelIndex(index) for index in selectedRows]
            for index in indexes:
                model.removeRow(index.row())

            if model.rowCount() == 0:
                model.insertRows(0, 1)
            elif not self.valueChecker.isLastRowEmpty():
                model.insertRows(model.rowCount(), 1)

        self.refreshCoordsMatrix(self.prev_row)
        self.highLightFeature(self.prev_row, 0)

    def addPartButtonClicked(self):
        self.__contursCount = self.__contursCount + 1
        self.listParts.addItem(str(self.__contursCount))
        element = [self.__contursCount, list()]
        self.coords_matrix.append(element)

    def addRingButtonClicked(self):
        self.__ringsCount = self.__ringsCount + 1
        self.listParts.addItem(str(-self.__ringsCount))
        element = [-self.__ringsCount, list()]
        self.coords_matrix.append(element)

    def removePartButtonClicked(self):
        l_currentRow = self.listParts.currentRow()
        deletedPartNumber = int(self.listParts.item(l_currentRow).text())
        self.prev_row = -1

        if deletedPartNumber > 0:
            self.__contursCount = self.__contursCount - 1
        else:
            self.__ringsCount = self.__ringsCount - 1

        self.listParts.removeItemWidget(self.listParts.takeItem(l_currentRow))
        self.coords_matrix.remove(self.coords_matrix[l_currentRow])

        for i in range(self.listParts.count()):
            currentPartNumber = int(self.listParts.item(i).text())
            if deletedPartNumber > 0:
                if deletedPartNumber < currentPartNumber:
                    self.listParts.item(i).setData(0, str(currentPartNumber - 1))
                    self.coords_matrix[i][0] = currentPartNumber - 1
            else:
                if deletedPartNumber > currentPartNumber:
                    self.listParts.item(i).setData(0, str(currentPartNumber + 1))
                    self.coords_matrix[i][0] = currentPartNumber + 1

        if self.__contursCount == 0:
            self.addPartButtonClicked()
            self.listParts.setCurrentRow(0)
            self.prev_row = 0
        else:
            # Need for cute event handling!
            self.prev_row = -1

    def refreshCoordsMatrix(self, part_num):
        self.coords_matrix[part_num][1].clear()
        rowtuple = []
        model = self.twPoints.model()

        if self.valueChecker.isLastRowEmpty() or not self.valueChecker.isRowValid(model.rowCount() - 1):
            skipLastRow = 1
        else:
            skipLastRow = 0

        for i in range(model.rowCount() - skipLastRow):
            rowtuple.clear()
            for j in range(model.columnCount()):
                if self.valueChecker.checkModelValue(i, j) == CellValue.ValueFloat:
                    rowtuple.append(model.data(model.index(i, j, QModelIndex()), QtCore.Qt.EditRole))
                else:
                    rowtuple.append("NaN")
            self.coords_matrix[part_num][1].append(list(rowtuple))

    def refreshTable(self, part_num):
        # Clear coord's table
        if -1 < part_num < len(self.coords_matrix):
            model = self.twPoints.model()
            coordslist = self.coords_matrix[part_num][1]

            model.removeRows(0, model.rowCount())
            model.insertRows(0, len(self.coords_matrix[part_num][1]) + 1)

            model.blockSignals(True)
            for i in range(len(coordslist)):
                for j in range(model.columnCount()):
                    model.setData(model.createIndex(i, j), QVariant(str(coordslist[i][j])))
            model.blockSignals(False)
            model.dataChanged.emit(model.createIndex(0, 0),
                                   model.createIndex(model.rowCount() - 1, model.columnCount() - 1))

    def partChanged(self, currentRow):
        # Set cellValueChanged semaphore
        self.__part_changing = True

        if self.prev_row != -1:
            # Save current part
            self.refreshCoordsMatrix(self.prev_row)

        self.refreshTable(currentRow)
        self.prev_row = currentRow

        self.highLightFeature(currentRow, 0)
        self.__part_changing = False

    def saveDialogSettings(self):
        settings = QSettings()
        # tell the world if the coord should be transformed into the layer crs
        if self.rb_ProjectCrs.isChecked():
            settings.setValue("NumericDigitize/checked", "rb_ProjectCrs")
        elif self.rb_OtherCrs.isChecked() and self.featureCrsId != -1:
            settings.setValue("NumericDigitize/checked", "rb_OtherCrs")
            settings.setValue("NumericDigitize/featureCrsId", self.featureCrsId)
        else:
            settings.setValue("NumericDigitize/checked", "rb_LayerCrs")

    def onOK(self):
        # Refresh matrix coords for current part
        if self.prev_row != -1:
            self.refreshCoordsMatrix(self.prev_row)

        if not self.valueChecker.checkCoordsMatrix(self.coords_matrix):
            return

        if not self.valueChecker.isCurrentPartValid(True):
            QMessageBox.critical(self.window(),
                                 self.translate_str("Values error"),
                                 self.translate_str("Current part contains incorrect values"))
            return
        else:
            self.accept()

        self.saveDialogSettings()

        self.returnCoordList.emit(self.coords_matrix)

    def onFinished(self, result):
        if self.highLighter is not None:
            self.highLighter.removeHighlight()
            self.highLighter = None
