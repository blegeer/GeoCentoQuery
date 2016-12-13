# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GeoCentoThumbnail.ui'
#
# Created: Tue Dec 13 10:34:41 2016
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_GeoCentoThumbnailView(object):
    def setupUi(self, GeoCentoThumbnailView):
        GeoCentoThumbnailView.setObjectName(_fromUtf8("GeoCentoThumbnailView"))
        GeoCentoThumbnailView.resize(494, 373)
        self.thumbnailWebView = QtWebKit.QWebView(GeoCentoThumbnailView)
        self.thumbnailWebView.setGeometry(QtCore.QRect(10, 10, 471, 351))
        self.thumbnailWebView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.thumbnailWebView.setObjectName(_fromUtf8("thumbnailWebView"))

        self.retranslateUi(GeoCentoThumbnailView)
        QtCore.QMetaObject.connectSlotsByName(GeoCentoThumbnailView)

    def retranslateUi(self, GeoCentoThumbnailView):
        GeoCentoThumbnailView.setWindowTitle(_translate("GeoCentoThumbnailView", "GeoCento Thumbnail", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	GeoCentoThumbnailView = QtGui.QDialog()
	ui = GeoCentoThumbnail.Ui_GeoCentoThumbnailView()
	ui.setupUi(GeoCentoThumbnailView)
	GeoCentoThumbnailView.show()
	ui.thumbnailWebView.load(QtCore.QUrl("http://www.google.com"))
	sys.exit(app.exec_())

