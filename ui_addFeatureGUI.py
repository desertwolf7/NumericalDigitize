# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addFeatureGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_numericalDigitize_MainDialog(object):
    def setupUi(self, numericalDigitize_MainDialog):
        numericalDigitize_MainDialog.setObjectName("numericalDigitize_MainDialog")
        numericalDigitize_MainDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        numericalDigitize_MainDialog.resize(360, 464)
        numericalDigitize_MainDialog.setToolTip("")
        numericalDigitize_MainDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.gridLayout = QtWidgets.QGridLayout(numericalDigitize_MainDialog)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(numericalDigitize_MainDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rb_LayerCrs = QtWidgets.QRadioButton(self.groupBox)
        self.rb_LayerCrs.setChecked(True)
        self.rb_LayerCrs.setObjectName("rb_LayerCrs")
        self.verticalLayout.addWidget(self.rb_LayerCrs)
        self.rb_ProjectCrs = QtWidgets.QRadioButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rb_ProjectCrs.sizePolicy().hasHeightForWidth())
        self.rb_ProjectCrs.setSizePolicy(sizePolicy)
        self.rb_ProjectCrs.setChecked(False)
        self.rb_ProjectCrs.setObjectName("rb_ProjectCrs")
        self.verticalLayout.addWidget(self.rb_ProjectCrs)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rb_OtherCrs = QtWidgets.QRadioButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rb_OtherCrs.sizePolicy().hasHeightForWidth())
        self.rb_OtherCrs.setSizePolicy(sizePolicy)
        self.rb_OtherCrs.setObjectName("rb_OtherCrs")
        self.horizontalLayout.addWidget(self.rb_OtherCrs)
        self.l_OtherCrsName = QtWidgets.QLabel(self.groupBox)
        self.l_OtherCrsName.setObjectName("l_OtherCrsName")
        self.horizontalLayout.addWidget(self.l_OtherCrsName)
        self.pb_OtherCrs = QtWidgets.QPushButton(self.groupBox)
        self.pb_OtherCrs.setObjectName("pb_OtherCrs")
        self.horizontalLayout.addWidget(self.pb_OtherCrs)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.groupBox, 6, 1, 1, 1)
        self.gridMainLayout = QtWidgets.QGridLayout()
        self.gridMainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridMainLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridMainLayout.setHorizontalSpacing(3)
        self.gridMainLayout.setVerticalSpacing(0)
        self.gridMainLayout.setObjectName("gridMainLayout")
        self.partsFrame = QtWidgets.QFrame(numericalDigitize_MainDialog)
        self.partsFrame.setMinimumSize(QtCore.QSize(0, 100))
        self.partsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.partsFrame.setObjectName("partsFrame")
        self.partsFrameLayout = QtWidgets.QVBoxLayout(self.partsFrame)
        self.partsFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.partsFrameLayout.setSpacing(0)
        self.partsFrameLayout.setObjectName("partsFrameLayout")
        self.labelPart = QtWidgets.QLabel(self.partsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPart.sizePolicy().hasHeightForWidth())
        self.labelPart.setSizePolicy(sizePolicy)
        self.labelPart.setMinimumSize(QtCore.QSize(60, 25))
        self.labelPart.setMaximumSize(QtCore.QSize(60, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.labelPart.setFont(font)
        self.labelPart.setObjectName("labelPart")
        self.partsFrameLayout.addWidget(self.labelPart)
        self.listParts = QtWidgets.QListWidget(self.partsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listParts.sizePolicy().hasHeightForWidth())
        self.listParts.setSizePolicy(sizePolicy)
        self.listParts.setMinimumSize(QtCore.QSize(60, 0))
        self.listParts.setMaximumSize(QtCore.QSize(60, 16777215))
        self.listParts.setObjectName("listParts")
        self.partsFrameLayout.addWidget(self.listParts)
        self.gridMainLayout.addWidget(self.partsFrame, 0, 0, 1, 1)
        self.twPoints = QtWidgets.QTableWidget(numericalDigitize_MainDialog)
        self.twPoints.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.twPoints.setObjectName("twPoints")
        self.twPoints.setColumnCount(2)
        self.twPoints.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.twPoints.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.twPoints.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.twPoints.setHorizontalHeaderItem(1, item)
        self.gridMainLayout.addWidget(self.twPoints, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridMainLayout, 4, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(numericalDigitize_MainDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 1, 1, 1)
        self.frameButtons = QtWidgets.QFrame(numericalDigitize_MainDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameButtons.sizePolicy().hasHeightForWidth())
        self.frameButtons.setSizePolicy(sizePolicy)
        self.frameButtons.setMinimumSize(QtCore.QSize(0, 40))
        self.frameButtons.setMaximumSize(QtCore.QSize(350, 40))
        self.frameButtons.setObjectName("frameButtons")
        self.buttonsFrameLayout = QtWidgets.QHBoxLayout(self.frameButtons)
        self.buttonsFrameLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.buttonsFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsFrameLayout.setObjectName("buttonsFrameLayout")
        self.partButtonsFrame = QtWidgets.QFrame(self.frameButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.partButtonsFrame.sizePolicy().hasHeightForWidth())
        self.partButtonsFrame.setSizePolicy(sizePolicy)
        self.partButtonsFrame.setMinimumSize(QtCore.QSize(115, 40))
        self.partButtonsFrame.setMaximumSize(QtCore.QSize(115, 40))
        self.partButtonsFrame.setObjectName("partButtonsFrame")
        self.partButtonsLayout = QtWidgets.QHBoxLayout(self.partButtonsFrame)
        self.partButtonsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.partButtonsLayout.setContentsMargins(5, 0, 10, 0)
        self.partButtonsLayout.setObjectName("partButtonsLayout")
        self.toolButtonAddPart = QtWidgets.QToolButton(self.partButtonsFrame)
        self.toolButtonAddPart.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButtonAddPart.setMaximumSize(QtCore.QSize(32, 32))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/numericalDigitize/images/mActionAddPart.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonAddPart.setIcon(icon)
        self.toolButtonAddPart.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonAddPart.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButtonAddPart.setObjectName("toolButtonAddPart")
        self.partButtonsLayout.addWidget(self.toolButtonAddPart)
        self.toolButtonRemovePart = QtWidgets.QToolButton(self.partButtonsFrame)
        self.toolButtonRemovePart.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButtonRemovePart.setMaximumSize(QtCore.QSize(32, 32))
        self.toolButtonRemovePart.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/plugins/numericalDigitize/images/mActionDeletePart.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonRemovePart.setIcon(icon1)
        self.toolButtonRemovePart.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonRemovePart.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButtonRemovePart.setObjectName("toolButtonRemovePart")
        self.partButtonsLayout.addWidget(self.toolButtonRemovePart)
        self.toolButtonAddRing = QtWidgets.QToolButton(self.partButtonsFrame)
        self.toolButtonAddRing.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButtonAddRing.setMaximumSize(QtCore.QSize(32, 32))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/plugins/numericalDigitize/images/mActionAddRing.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonAddRing.setIcon(icon2)
        self.toolButtonAddRing.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonAddRing.setObjectName("toolButtonAddRing")
        self.partButtonsLayout.addWidget(self.toolButtonAddRing)
        self.buttonsFrameLayout.addWidget(self.partButtonsFrame, 0, QtCore.Qt.AlignLeft)
        self.rowButtonsFrame = QtWidgets.QFrame(self.frameButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rowButtonsFrame.sizePolicy().hasHeightForWidth())
        self.rowButtonsFrame.setSizePolicy(sizePolicy)
        self.rowButtonsFrame.setMinimumSize(QtCore.QSize(185, 40))
        self.rowButtonsFrame.setMaximumSize(QtCore.QSize(185, 40))
        self.rowButtonsFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.rowButtonsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rowButtonsFrame.setLineWidth(0)
        self.rowButtonsFrame.setObjectName("rowButtonsFrame")
        self.buttonsRowLayout = QtWidgets.QHBoxLayout(self.rowButtonsFrame)
        self.buttonsRowLayout.setContentsMargins(5, 0, 10, 0)
        self.buttonsRowLayout.setObjectName("buttonsRowLayout")
        self.toolButtonCopy = QtWidgets.QToolButton(self.rowButtonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButtonCopy.sizePolicy().hasHeightForWidth())
        self.toolButtonCopy.setSizePolicy(sizePolicy)
        self.toolButtonCopy.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButtonCopy.setMaximumSize(QtCore.QSize(32, 32))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/plugins/numericalDigitize/images/mActionEditCopy.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonCopy.setIcon(icon3)
        self.toolButtonCopy.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonCopy.setObjectName("toolButtonCopy")
        self.buttonsRowLayout.addWidget(self.toolButtonCopy)
        self.toolButtonPaste = QtWidgets.QToolButton(self.rowButtonsFrame)
        self.toolButtonPaste.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButtonPaste.setMaximumSize(QtCore.QSize(32, 32))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/plugins/numericalDigitize/images/mActionEditPaste.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonPaste.setIcon(icon4)
        self.toolButtonPaste.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonPaste.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButtonPaste.setObjectName("toolButtonPaste")
        self.buttonsRowLayout.addWidget(self.toolButtonPaste)
        self.toolButtonSwap = QtWidgets.QToolButton(self.rowButtonsFrame)
        self.toolButtonSwap.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButtonSwap.setMaximumSize(QtCore.QSize(32, 32))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/plugins/numericalDigitize/images/swap.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonSwap.setIcon(icon5)
        self.toolButtonSwap.setIconSize(QtCore.QSize(24, 24))
        self.toolButtonSwap.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButtonSwap.setObjectName("toolButtonSwap")
        self.buttonsRowLayout.addWidget(self.toolButtonSwap)
        self.toolButtonAddRows = QtWidgets.QToolButton(self.rowButtonsFrame)
        self.toolButtonAddRows.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButtonAddRows.setMaximumSize(QtCore.QSize(32, 32))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/plugins/numericalDigitize/images/mActionNewTableRow.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonAddRows.setIcon(icon6)
        self.toolButtonAddRows.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonAddRows.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButtonAddRows.setObjectName("toolButtonAddRows")
        self.buttonsRowLayout.addWidget(self.toolButtonAddRows, 0, QtCore.Qt.AlignLeft)
        self.toolButtonRemoveRows = QtWidgets.QToolButton(self.rowButtonsFrame)
        self.toolButtonRemoveRows.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButtonRemoveRows.setMaximumSize(QtCore.QSize(32, 32))
        self.toolButtonRemoveRows.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/plugins/numericalDigitize/images/mActionDeleteTableRow.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonRemoveRows.setIcon(icon7)
        self.toolButtonRemoveRows.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonRemoveRows.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButtonRemoveRows.setObjectName("toolButtonRemoveRows")
        self.buttonsRowLayout.addWidget(self.toolButtonRemoveRows)
        self.buttonsFrameLayout.addWidget(self.rowButtonsFrame, 0, QtCore.Qt.AlignLeft)
        self.reprojectFrame = QtWidgets.QFrame(self.frameButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reprojectFrame.sizePolicy().hasHeightForWidth())
        self.reprojectFrame.setSizePolicy(sizePolicy)
        self.reprojectFrame.setMinimumSize(QtCore.QSize(40, 40))
        self.reprojectFrame.setMaximumSize(QtCore.QSize(40, 40))
        self.reprojectFrame.setObjectName("reprojectFrame")
        self.reprojectLayout = QtWidgets.QHBoxLayout(self.reprojectFrame)
        self.reprojectLayout.setContentsMargins(5, 0, 10, 0)
        self.reprojectLayout.setObjectName("reprojectLayout")
        self.toolButtonReproject = QtWidgets.QToolButton(self.reprojectFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(32)
        sizePolicy.setVerticalStretch(32)
        sizePolicy.setHeightForWidth(self.toolButtonReproject.sizePolicy().hasHeightForWidth())
        self.toolButtonReproject.setSizePolicy(sizePolicy)
        self.toolButtonReproject.setMinimumSize(QtCore.QSize(32, 32))
        self.toolButtonReproject.setMaximumSize(QtCore.QSize(32, 32))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/plugins/numericalDigitize/images/mActionSetProjection.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonReproject.setIcon(icon8)
        self.toolButtonReproject.setIconSize(QtCore.QSize(32, 32))
        self.toolButtonReproject.setObjectName("toolButtonReproject")
        self.reprojectLayout.addWidget(self.toolButtonReproject)
        self.buttonsFrameLayout.addWidget(self.reprojectFrame, 0, QtCore.Qt.AlignLeft)
        self.rowButtonsFrame.raise_()
        self.partButtonsFrame.raise_()
        self.reprojectFrame.raise_()
        self.gridLayout.addWidget(self.frameButtons, 0, 1, 1, 1)

        self.retranslateUi(numericalDigitize_MainDialog)
        self.buttonBox.rejected.connect(numericalDigitize_MainDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(numericalDigitize_MainDialog)

    def retranslateUi(self, numericalDigitize_MainDialog):
        _translate = QtCore.QCoreApplication.translate
        numericalDigitize_MainDialog.setWindowTitle(_translate("numericalDigitize_MainDialog", "Add numerical feature"))
        self.groupBox.setTitle(_translate("numericalDigitize_MainDialog", "Coordinates are given"))
        self.rb_LayerCrs.setText(_translate("numericalDigitize_MainDialog", "in the CRS of the Layer"))
        self.rb_ProjectCrs.setText(_translate("numericalDigitize_MainDialog", "in the CRS of the Project"))
        self.rb_OtherCrs.setText(_translate("numericalDigitize_MainDialog", "other"))
        self.l_OtherCrsName.setText(_translate("numericalDigitize_MainDialog", "not selected"))
        self.pb_OtherCrs.setText(_translate("numericalDigitize_MainDialog", "Select"))
        self.labelPart.setText(_translate("numericalDigitize_MainDialog", "Part №"))
        item = self.twPoints.verticalHeaderItem(0)
        item.setText(_translate("numericalDigitize_MainDialog", "1"))
        item = self.twPoints.horizontalHeaderItem(0)
        item.setText(_translate("numericalDigitize_MainDialog", "X"))
        item = self.twPoints.horizontalHeaderItem(1)
        item.setText(_translate("numericalDigitize_MainDialog", "Y"))
        self.toolButtonAddPart.setToolTip(_translate("numericalDigitize_MainDialog", "Add part"))
        self.toolButtonAddPart.setText(_translate("numericalDigitize_MainDialog", "..."))
        self.toolButtonRemovePart.setToolTip(_translate("numericalDigitize_MainDialog", "Remove part"))
        self.toolButtonRemovePart.setText(_translate("numericalDigitize_MainDialog", "..."))
        self.toolButtonAddRing.setToolTip(_translate("numericalDigitize_MainDialog", "Add polygon ring"))
        self.toolButtonAddRing.setText(_translate("numericalDigitize_MainDialog", "..."))
        self.toolButtonCopy.setToolTip(_translate("numericalDigitize_MainDialog", "Copy to clipboard"))
        self.toolButtonCopy.setText(_translate("numericalDigitize_MainDialog", "..."))
        self.toolButtonPaste.setToolTip(_translate("numericalDigitize_MainDialog", "Paste from clipboard"))
        self.toolButtonPaste.setText(_translate("numericalDigitize_MainDialog", "..."))
        self.toolButtonSwap.setToolTip(_translate("numericalDigitize_MainDialog", "Swap values of X and Y columns"))
        self.toolButtonSwap.setText(_translate("numericalDigitize_MainDialog", "..."))
        self.toolButtonAddRows.setToolTip(_translate("numericalDigitize_MainDialog", "Add row"))
        self.toolButtonAddRows.setText(_translate("numericalDigitize_MainDialog", "..."))
        self.toolButtonRemoveRows.setToolTip(_translate("numericalDigitize_MainDialog", "Delete rows"))
        self.toolButtonRemoveRows.setText(_translate("numericalDigitize_MainDialog", "..."))
        self.toolButtonReproject.setText(_translate("numericalDigitize_MainDialog", "..."))

