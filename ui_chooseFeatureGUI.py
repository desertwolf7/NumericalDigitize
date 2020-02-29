# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chooseFeatureGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_chooseFeatureDialog(object):
    def setupUi(self, chooseFeatureDialog):
        chooseFeatureDialog.setObjectName("chooseFeatureDialog")
        chooseFeatureDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        chooseFeatureDialog.resize(470, 391)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(chooseFeatureDialog.sizePolicy().hasHeightForWidth())
        chooseFeatureDialog.setSizePolicy(sizePolicy)
        chooseFeatureDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        chooseFeatureDialog.setSizeGripEnabled(False)
        self.gridLayout = QtWidgets.QGridLayout(chooseFeatureDialog)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(chooseFeatureDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setMinimumSize(QtCore.QSize(0, 30))
        self.buttonBox.setMaximumSize(QtCore.QSize(16777215, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.listFeatures = QtWidgets.QListWidget(chooseFeatureDialog)
        self.listFeatures.setObjectName("listFeatures")
        self.gridLayout.addWidget(self.listFeatures, 0, 0, 1, 1)

        self.retranslateUi(chooseFeatureDialog)
        self.buttonBox.accepted.connect(chooseFeatureDialog.accept)
        self.buttonBox.rejected.connect(chooseFeatureDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(chooseFeatureDialog)

    def retranslateUi(self, chooseFeatureDialog):
        _translate = QtCore.QCoreApplication.translate
        chooseFeatureDialog.setWindowTitle(_translate("chooseFeatureDialog", "Choose feature for edit"))

