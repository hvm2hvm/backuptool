import sys

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QAbstractItemModel, QVariant, QModelIndex, QString
from PyQt4.uic import loadUiType

BackupUiBase, BUiQtBase = loadUiType("main.ui")

class BackupUi(BackupUiBase, BUiQtBase):

    def __init__(self):
        BUiQtBase.__init__(self)
        
        self.setupUi(self)
        
        self.sourceView.setModel(FileModel('bla'))

class FileModel(QAbstractItemModel):

    def __init__(self, data):
        QAbstractItemModel.__init__(self)
        self.data = data
        
    def index(self, row, column, parent):
        print "index:: row: %s, column: %s, parent: %s/%s/%s" % (row, column, parent.isValid(), parent.row(), parent.column())
        if not parent.isValid():
            return self.createIndex(row, column)
        else:
            return QModelIndex()
        
    def parent(self, child):
        print "parent:: child: %s/%s/%s" % (child.isValid(), child.row(), child.column())
        return QModelIndex()
        
    def rowCount(self, parent):
        print "rowCount:: parent: %s/%s/%s" % (parent.isValid(), parent.row(), parent.column())
        if not parent.isValid():
            return 5
        else:
            return 0
            
    def columnCount(self, parent):
        print "columnCount:: parent: %s/%s/%s" % (parent.isValid(), parent.row(), parent.column())
        if not parent.isValid():
            return 2
        else:
            return 0
            
    def data(self, index, role):
        print "data:: index: %s/%s/%s, role: %s" % (index.isValid(), index.row(), index.column(), role)
        if index.isValid():
            return QVariant("%s/%s" % (index.row, index.column))
        else:
            return QVariant.Type.Invalid
        
app = QApplication(sys.argv)
    
main = BackupUi()
main.show()

app.exec_()
