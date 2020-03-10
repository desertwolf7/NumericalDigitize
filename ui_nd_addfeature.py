# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nd_addfeature.ui'
#
# Created: Sun Apr 12 21:08:43 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Nd_AddFeature(object):
    def setupUi(self, Nd_AddFeature):
        Nd_AddFeature.setObjectName(_fromUtf8("Nd_AddFeature"))
        Nd_AddFeature.setWindowModality(QtCore.Qt.ApplicationModal)
        Nd_AddFeature.resize(389, 404)
        self.gridLayout = QtGui.QGridLayout(Nd_AddFeature)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblNumericalFeature = QtGui.QLabel(Nd_AddFeature)
        self.lblNumericalFeature.setObjectName(_fromUtf8("lblNumericalFeature"))
        self.gridLayout.addWidget(self.lblNumericalFeature, 0, 0, 1, 1)
        self.twPoints = QtGui.QTableWidget(Nd_AddFeature)
        self.twPoints.setObjectName(_fromUtf8("twPoints"))
        self.twPoints.setColumnCount(2)
        self.twPoints.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.twPoints.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.twPoints.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.twPoints.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.twPoints, 1, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(Nd_AddFeature)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.rb_ProjectCrs = QtGui.QRadioButton(self.groupBox)
        self.rb_ProjectCrs.setChecked(True)
        self.rb_ProjectCrs.setObjectName(_fromUtf8("rb_ProjectCrs"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.rb_ProjectCrs)
        self.rb_LayerCrs = QtGui.QRadioButton(self.groupBox)
        self.rb_LayerCrs.setObjectName(_fromUtf8("rb_LayerCrs"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.rb_LayerCrs)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setContentsMargins(-1, -1, 0, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.rb_OtherCrs = QtGui.QRadioButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rb_OtherCrs.sizePolicy().hasHeightForWidth())
        self.rb_OtherCrs.setSizePolicy(sizePolicy)
        self.rb_OtherCrs.setObjectName(_fromUtf8("rb_OtherCrs"))
        self.horizontalLayout.addWidget(self.rb_OtherCrs)
        self.l_OtherCrsName = QtGui.QLabel(self.groupBox)
        self.l_OtherCrsName.setObjectName(_fromUtf8("l_OtherCrsName"))
        self.horizontalLayout.addWidget(self.l_OtherCrsName)
        self.pb_ChooseCrs = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_ChooseCrs.sizePolicy().hasHeightForWidth())
        self.pb_ChooseCrs.setSizePolicy(sizePolicy)
        self.pb_ChooseCrs.setObjectName(_fromUtf8("pb_ChooseCrs"))
        self.horizontalLayout.addWidget(self.pb_ChooseCrs)
        self.formLayout_2.setLayout(2, QtGui.QFormLayout.SpanningRole, self.horizontalLayout)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Nd_AddFeature)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(Nd_AddFeature)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Nd_AddFeature.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Nd_AddFeature.reject)
        QtCore.QMetaObject.connectSlotsByName(Nd_AddFeature)

    def retranslateUi(self, Nd_AddFeature):
        Nd_AddFeature.setWindowTitle(_translate("Nd_AddFeature", "Add numerical feature", None))
        self.lblNumericalFeature.setText(_translate("Nd_AddFeature", "Add a numerical feature:", None))
        item = self.twPoints.verticalHeaderItem(0)
        item.setText(_translate("Nd_AddFeature", "1", None))
        item = self.twPoints.horizontalHeaderItem(0)
        item.setText(_translate("Nd_AddFeature", "X", None))
        item = self.twPoints.horizontalHeaderItem(1)
        item.setText(_translate("Nd_AddFeature", "Y", None))
        self.groupBox.setTitle(_translate("Nd_AddFeature", "Coordinates are given", None))
        self.rb_ProjectCrs.setText(_translate("Nd_AddFeature", "in the CRS of theProject", None))
        self.rb_LayerCrs.setText(_translate("Nd_AddFeature", "in the CRS of the Layer", None))
        self.rb_OtherCrs.setText(_translate("Nd_AddFeature", "other", None))
        self.l_OtherCrsName.setText(_translate("Nd_AddFeature", "not selected", None))
        self.pb_ChooseCrs.setText(_translate("Nd_AddFeature", "Select", None))

