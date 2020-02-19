import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import pyqtSlot
from TG43_GUI_v1_3 import Ui_Dialog
import TG43

class AppWindow(QDialog):

    source_list = []
    refpoint_list = []

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()

    def getSourcePos(self):
        x, y, z, activity, time = round(self.ui.source_x.value(), 1),\
                                  round(self.ui.source_y.value(), 1),\
                                  round(self.ui.source_z.value(), 1),\
                                  round(self.ui.source_activity.value(), 1),\
                                  round(self.ui.source_time.value(), 1)
        return x, y, z, activity, time


    def addSource(self):

        x, y, z = round(self.ui.source_x.value(), 1),\
                  round(self.ui.source_y.value(), 1),\
                  round(self.ui.source_z.value(), 1)
        activity = round(self.ui.source_activity.value(), 1)
        time = round(self.ui.source_time.value(), 1)
        source = TG43.Source(x, y, z, activity, time)
        self.source_list.append(source)
        row_pos = self.ui.source_table.rowCount()
        self.ui.source_table.insertRow(row_pos)
        self.ui.source_table.setItem(row_pos, 0, QtWidgets.QTableWidgetItem(str(source.type)))
        self.ui.source_table.setItem(row_pos, 1, QtWidgets.QTableWidgetItem(str(x)))
        self.ui.source_table.setItem(row_pos, 2, QtWidgets.QTableWidgetItem(str(y)))
        self.ui.source_table.setItem(row_pos, 3, QtWidgets.QTableWidgetItem(str(z)))
        self.ui.source_table.setItem(row_pos, 4, QtWidgets.QTableWidgetItem(str(activity)))
        self.ui.source_table.setItem(row_pos, 5, QtWidgets.QTableWidgetItem(str(time)))

    def addRefPoint(self):
        _translate = QtCore.QCoreApplication.translate
        x, y, z = round(self.ui.dose_ref_x.value(), 1),\
                  round(self.ui.dose_ref_y.value(), 1),\
                  round(self.ui.dose_ref_z.value(), 1)
        ref = TG43.DoseRefPoint(x, y, z)
        dose = ref.computeDose(self.source_list)
        self.refpoint_list.append(ref)
        row_pos = self.ui.refpoint_table.rowCount()
        self.ui.refpoint_table.insertRow(row_pos)
        self.ui.refpoint_table.setItem(row_pos, 0, QtWidgets.QTableWidgetItem(str(x)))
        self.ui.refpoint_table.setItem(row_pos, 1, QtWidgets.QTableWidgetItem(str(y)))
        self.ui.refpoint_table.setItem(row_pos, 2, QtWidgets.QTableWidgetItem(str(z)))
        self.ui.refpoint_table.setItem(row_pos, 3, QtWidgets.QTableWidgetItem(str(round(np.sum(dose), 2))))

    def runExample(self):
        """
        Function used to run example for project
        TODO will need to clear table and create sources/ref points at predefined locations
        """
        self.ui.refpoint_table.setRowCount(0)
        self.ui.source_table.setRowCount(0)
        self.source_list = [TG43.Source(0, 0, 0, 10, 10),
                            TG43.Source(0, 2, 0, 10, 10),
                            TG43.Source(0, -2, 0, 10, 10),
                            TG43.Source(3, 1, 0, 10, 10),
                            TG43.Source(3, -1, 0, 10, 10)]
        row_pos = 0
        for source in self.source_list:
            self.ui.source_table.insertRow(row_pos)
            self.ui.source_table.setItem(row_pos, 0, QtWidgets.QTableWidgetItem(str(source.type)))
            self.ui.source_table.setItem(row_pos, 1, QtWidgets.QTableWidgetItem(str(source.x)))
            self.ui.source_table.setItem(row_pos, 2, QtWidgets.QTableWidgetItem(str(source.y)))
            self.ui.source_table.setItem(row_pos, 3, QtWidgets.QTableWidgetItem(str(source.z)))
            self.ui.source_table.setItem(row_pos, 4, QtWidgets.QTableWidgetItem(str(source.activity)))
            self.ui.source_table.setItem(row_pos, 5, QtWidgets.QTableWidgetItem(str(source.time)))
            row_pos += 1

        self.refpoint_list = []

        self.refpoint_list = [TG43.DoseRefPoint(-2.0, 0, 0),
                              TG43.DoseRefPoint(1.5, 0, 0),
                              TG43.DoseRefPoint(1.5, 3, 0),
                              TG43.DoseRefPoint(1.5, 4, 0),
                              TG43.DoseRefPoint(4, 0, 0)]

        row_pos = 0
        for refpoint in self.refpoint_list:
            self.ui.refpoint_table.insertRow(row_pos)
            self.ui.refpoint_table.setItem(row_pos, 0, QtWidgets.QTableWidgetItem(str(refpoint.x)))
            self.ui.refpoint_table.setItem(row_pos, 1, QtWidgets.QTableWidgetItem(str(refpoint.y)))
            self.ui.refpoint_table.setItem(row_pos, 2, QtWidgets.QTableWidgetItem(str(refpoint.z)))
            self.ui.refpoint_table.setItem(row_pos, 3, QtWidgets.QTableWidgetItem(str(round(np.sum(refpoint.computeDose(self.source_list)), 2))))
            row_pos += 1


    def clearRefPoint(self):
        self.ui.refpoint_table.setRowCount(0)
        self.refpoint_list = []

    def clearSources(self):
        self.ui.source_table.setRowCount(0)
        self.source_list = []

    def addGraphics(self):
        pass


app = QApplication(sys.argv)
w = AppWindow()
w.show()

w.ui.add_source.clicked.connect(w.addSource)
w.ui.add_dose_point.clicked.connect(w.addRefPoint)
w.ui.close_all.clicked.connect(QtWidgets.qApp.closeAllWindows)
w.ui.run_example.clicked.connect(w.runExample)
w.ui.delete_refpoint.clicked.connect(w.clearRefPoint)
w.ui.delete_source.clicked.connect(w.clearSources)

sys.exit(app.exec_())