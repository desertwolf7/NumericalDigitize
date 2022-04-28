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

from qgis.PyQt.QtCore import (QVariant, QCoreApplication, QMetaType, QModelIndex)
from qgis.PyQt.QtWidgets import QMessageBox, QDialog
from qgis.core import QgsVectorLayer

from .resources import *
from .ui_chooseFeatureGUI import Ui_chooseFeatureDialog

import os
from builtins import int, str

# noinspection PyPep8Naming
class ChooseFeatureGUI(QDialog, Ui_chooseFeatureDialog):

    def __init__(self, parent=None):
        """Constructor."""
        super(ChooseFeatureGUI, self).__init__(parent)
        self.setupUi(self)

        self.selectedFeature = 0
        self.__localFeatureList = None
        self.__layer = None
        self.listFeatures.currentRowChanged.connect(self.onFeatureChanged)

    def configureDialog(self, featureList: list, layer: QgsVectorLayer):
        # featureList - list of QgsFeature

        self.__layer = layer
        self.__localFeatureList = list(featureList)
        displayFieldsList = self.selectDisplayFields()

        model = self.listFeatures.model()
        model.blockSignals(True)
        model.insertRows(0, len(self.__localFeatureList))

        for i in range(len(self.__localFeatureList)):
            textValue = self.translate_str('Feature with Id = ') + str(self.__localFeatureList[i].id()) + '; '
            if len(displayFieldsList) > 0:
                attributeValue = ""
                for j in range(len(displayFieldsList)):
                    attributeValue = str(self.__localFeatureList[i][displayFieldsList[j][0]])
                    if len(attributeValue) > 0 and attributeValue != "NULL":
                        break
                textValue = textValue + " (" +attributeValue + ")"

            model.setData(model.index(i, 0, QModelIndex()), textValue)

        model.blockSignals(False)
        model.dataChanged.emit(model.index(0, 0, QModelIndex()), model.index(model.rowCount() - 1, 0, QModelIndex()))

        self.selectedFeature = 0
        self.__layer.select(self.__localFeatureList[self.selectedFeature].id())

    def configureSignals(self):
        # When OK pressed
        self.buttonBox.accepted.connect(self.onOK)
        self.buttonBox.rejected.connect(self.onReject)

    def clearControls(self):
        model = self.listFeatures.model()
        model.removeRows(0, model.rowCount())

    def selectDisplayFields(self):

        numTypes = [QMetaType.Int, QMetaType.UInt, QMetaType.Double, QMetaType.Long, QMetaType.LongLong,
                    QMetaType.Short, QMetaType.ULong, QMetaType.ULongLong, QMetaType.UShort, QMetaType.Float]
        datetimeTypes = [QMetaType.QDate, QMetaType.QDateTime, QMetaType.QTime]

        displayFieldsList = list()
        priority = 0

        localFields = self.__layer.fields()
        # No fields in layer - display feature.id
        if localFields.count() == 0:
            return list()
        else:
            for i in range(len(localFields)):
                priority = 0
                # If at least one field in selected features not empty and can convert to string then continue
                if not self.fieldIsEmpty(i) and self.fieldCanConvertToStr(i) and \
                        (localFields.field(i).type() == QMetaType.QString or
                        localFields.field(i).type() in numTypes or
                        localFields.field(i).type() in datetimeTypes):

                    # If field name highly likely description of feature then increase priority
                    if self.fieldIsPreferred(localFields.field(i).name()):
                        priority = priority + 50
                    # Try to exclude too long fields
                    if localFields.field(i).length() > 256:
                        priority = priority - 10
                    # Increase priority for string type
                    if localFields.field(i).type() == QMetaType.QString:
                        # Ignore single char fields
                        if localFields.field(i).length() > -1:
                            priority = priority + 10
                    if localFields.field(i).type() in numTypes:
                        priority = priority - 5
                    if localFields.field(i).type() in datetimeTypes:
                        priority = priority - 10

                    displayFieldsList.append([i, priority])

            if len(displayFieldsList) > 0:
                displayFieldsList.sort(key=lambda x: x[1], reverse=True)

            return displayFieldsList

    def fieldIsEmpty(self, fieldIndex):
        isEmpty = True
        for i in range(len(self.__localFeatureList)):
            isEmpty = isEmpty and QVariant(self.__localFeatureList[i][fieldIndex]).isNull()

        return isEmpty

    def fieldCanConvertToStr(self, fieldIndex):
        canConvert = True
        for i in range(len(self.__localFeatureList)):
            canConvert = canConvert and QVariant(self.__localFeatureList[i][fieldIndex]).convert(QVariant.String)

        return canConvert

    def fieldIsPreferred(self, fieldName):
        preferredFieldNames = ['name', 'description', 'address', 'note']
        isPreferred = False
        for i in range(len(preferredFieldNames)):
            isPreferred = isPreferred or (fieldName.lower().find(preferredFieldNames[i].lower()) != -1)

        return isPreferred

    @staticmethod
    def translate_str(message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("ChooseFeatureGUI", message)

    def onFeatureChanged(self, currentRow):
        if currentRow != -1:
            if self.selectedFeature != -1:
                self.__layer.deselect(self.__localFeatureList[self.selectedFeature].id())
            self.__layer.select(self.__localFeatureList[currentRow].id())
            self.selectedFeature = currentRow

    def onOK(self):
        self.__layer.deselect(self.__localFeatureList[self.selectedFeature].id())
        self.accept()

    def onReject(self):
        self.__layer.deselect(self.__localFeatureList[self.selectedFeature].id())
        self.reject()
