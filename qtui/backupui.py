import sys

from PyQt4.QtGui import QApplication, QTreeWidgetItem
from PyQt4.uic import loadUiType

BackupUiBase, BUiQtBase = loadUiType("main.ui")

class BackupUi(BackupUiBase, BUiQtBase):

    def __init__(self):
        BUiQtBase.__init__(self)
        
        self.setupUi(self)
        
        self.sourceView.setColumnCount(2)
        item = QTreeWidgetItem(["hello", "abc"])
        item.addChild(QTreeWidgetItem(["lalala", "la"]))
        self.sourceView.insertTopLevelItem(0, item)
        
app = QApplication(sys.argv)
    
main = BackupUi()
main.show()

app.exec_()
