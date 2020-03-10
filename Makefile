
all: resources.py ui_nd_addfeature.py ts lang

clean:
	rm -f ui_*.py resources.py
	rm -f *.pyc

ui_nd_addfeature.py: nd_addfeature.ui
	pyuic4 -o ui_nd_addfeature.py nd_addfeature.ui
#	
#ui_nonSpatialTablesDialogCols.py: nonSpatialTablesDialogCols.ui
#	pyuic4 -o ui_nonSpatialTablesDialogCols.py nonSpatialTablesDialogCols.ui
#	
#ui_nonSpatialTablesRename.py: nonSpatialTablesRename.ui
#	pyuic4 -o ui_nonSpatialTablesRename.py nonSpatialTablesRename.ui
#
resources.py: resources.qrc
	pyrcc4 -o resources.py resources.qrc

ts: numericalDigitize.pro
	pylupdate4 -verbose $<

lang: numericalDigitize.pro
	lrelease numericalDigitize.pro $<
