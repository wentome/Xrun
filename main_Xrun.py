from PySide import  QtGui
import sys

from manager import manager_class

class power_Form(QtGui.QWidget):
    def __init__(self):
        super(power_Form, self).__init__()
        self.M=manager_class(self)

    def closeEvent(self, event):
        self.M.close_process()


app = QtGui.QApplication(sys.argv)
p = power_Form()
p.show()
sys.exit(app.exec_())
