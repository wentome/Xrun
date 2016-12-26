from Xrun_ui import Ui_Form
from ovens import Ovens
from power import Power
from jdsu  import JDSU
from interacton import Interaction
from wdt import WDT
from PySide import QtCore
import json
from frigate import Cia

class manager_class(QtCore.QObject):
    def __init__(self,parent):
        super( manager_class,self).__init__()
        self.members = ['Ovens', 'Power', 'JDSU', 'IMB1','IMB2','LC1','LC2'] # member name must same with member class frigate init_nane
        self.put_ui(parent)
        self.sig_slot()
        self.cia=Cia()

        self.ovens=Ovens()
        self.power=Power()
        self.jdsu=JDSU()
        self.imb1 = Interaction('IMB1')
        self.imb2 = Interaction('IMB2')
        self.lc1 = Interaction('LC1')
        self.lc2 = Interaction('LC2')

        self.wdt=WDT(self.members)  # No need modify wdt.py

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.refresh)
        timer.start(1000)

    def put_ui(self,parent):
        self.ui = Ui_Form()
        self.ui.setupUi(parent)
        self.init_conf()
        for member in self.members: #save members WDT default stylesheet
            exec ('self.' + member.lower()+'_wdt_stylesheet =self.ui.'  + member.lower() + '_wdt.styleSheet()')

        self.jdsu_sync_stylesheet = self.ui.led_sync.styleSheet()
        self.jdsu_laser_on_stylesheet=self.ui.laser_on.styleSheet()
        self.jdsu_test_on_stylesheet = self.ui.test_on.styleSheet()
        self.ui.jdsu_tx.setDigitCount(20)
        self.ui.jdsu_error.setDigitCount(20)


    def sig_slot(self):
        for member in self.members:  # save members WDT default stylesheet
            exec ('self.ui.' + member.lower() + '_check.stateChanged.connect(self.' + member.lower() + '_action)')
            exec ('self.ui.' + member.lower() + '_wdt.stateChanged.connect(self.' + member.lower() + '_wdt)')

    ############################## uv_ov ####################################
    def close_process(self):
        temp = []
        for i in self.members:
            temp.append(i.lower() + '_addr')
        self.save_conf(temp, 'conf/sys.conf')

    def init_conf(self):
        temp = []
        for i in self.members:
            temp.append(i.lower() + '_addr')
        self.put_conf(temp, 'conf/sys.conf')

    def save_conf(self, members, name):
        test_conf = {}
        for i in members:
            test_conf[i] = eval('self.ui.' + i + '.text()')
        fc = open(name, 'w')
        json.dump(test_conf, fc)
        fc.close()

    def put_conf(self, members, name):
        try:
            fc = open(name, 'r')  # read previous  parameter from 'conf/uv_ov.conf'
            res = json.load(fc)
            fc.close()
            for i in members:
                eval('self.ui.' + i + '.setText(res[i])')
        except:
            print 'init conf failed'

    def refresh(self):
        try:
            self.ui.ovens_set.display(self.cia.data['Ovens']['set_temp'])
            self.ui.ovens_real.display(self.cia.data['Ovens']['real_temp'])
        except:
            pass
        try:
            self.ui.power_vol.display(float(self.cia.data['Power']['vol']))
            self.ui.power_cur.display(float(self.cia.data['Power']['cur']))
        except:
            pass
        try:
            if self.cia.data['JDSU']['sync']=='lost':
                self.ui.led_sync.setStyleSheet(self.jdsu_sync_stylesheet)
            elif self.cia.data['JDSU']['sync']=='found':
                self.ui.led_sync.setStyleSheet("background-color: rgb(0, 255, 0); ")
            elif self.cia.data['JDSU']['sync'] == 'hist':
                self.ui.led_sync.setStyleSheet("background-color: rgb(255, 255, 0); ")

            if self.cia.data['JDSU']['laser']=='ON':
                self.ui.laser_on.setStyleSheet("background-color: rgb(0, 255, 0); ")
            elif self.cia.data['JDSU']['laser']=='OFF':
                self.ui.laser_on.setStyleSheet(self.jdsu_laser_on_stylesheet)

            if self.cia.data['JDSU']['test']=='ON':
                self.ui.test_on.setStyleSheet("background-color: rgb(0, 255, 0); ")
            elif self.cia.data['JDSU']['test']=='OFF':
                self.ui.test_on.setStyleSheet(self.jdsu_test_on_stylesheet)

            self.ui.jdsu_tx.display(str(self.cia.data['JDSU']['tx']))
            self.ui.jdsu_error.display(str(self.cia.data['JDSU']['bit_error']))
        except:
            pass

        for member in self.members:
            if eval('self.wdt.'+member.lower()+'_wdt_active == True'):
                if eval('self.wdt.'+member.lower()+'_wdt_die == True'):
                    eval('self.ui.'+member.lower()+'_wdt.setStyleSheet("background-color: rgb(255, 0, 0); ")')
                else:
                    eval('self.ui.' + member.lower() + '_wdt.setStyleSheet("background-color: rgb(0, 255, 0); ")')
            else:
                eval('self.ui.' + member.lower() + '_wdt.setStyleSheet(self.'+ member.lower()+'_wdt_stylesheet)')


    def ovens_action(self):
        if self.ui.ovens_check.isChecked():
            self.ovens.ovens_run_start(self.ui.ovens_addr.text())
            self.ui.ovens_wdt.setChecked(True)
        else:
            self.ovens.ovens_run_stop()

    def power_action(self):
        if self.ui.power_check.isChecked():
            self.power.power_run_start(self.ui.power_addr.text())
            self.ui.power_wdt.setChecked(True)
        else:
            self.power.power_run_stop()
    def jdsu_action(self):
        if self.ui.jdsu_check.isChecked():
            self.jdsu.jdsu_run_start(self.ui.jdsu_addr.text())
            self.ui.jdsu_wdt.setChecked(True)
        else:
            self.jdsu.jdsu_run_stop()

    def imb1_action(self):
        if self.ui.imb1_check.isChecked():
            self.imb1.interaction_run_start(self.ui.imb1_addr.text())
            self.ui.imb1_wdt.setChecked(True)
        else:
            self.imb1.interaction_run_stop()
    def imb2_action(self):
        if self.ui.imb2_check.isChecked():
            self.imb2.interaction_run_start(self.ui.imb2_addr.text())
            self.ui.imb2_wdt.setChecked(True)
        else:
            self.imb2.interaction_run_stop()

    def lc1_action(self):
        if self.ui.lc1_check.isChecked():
            self.lc1.interaction_run_start(self.ui.lc1_addr.text())
            self.ui.lc1_wdt.setChecked(True)
        else:
            self.lc1.interaction_run_stop()

    def lc2_action(self):
        if self.ui.lc2_check.isChecked():
            self.lc2.interaction_run_start(self.ui.lc2_addr.text())
            self.ui.lc2_wdt.setChecked(True)
        else:
            self.lc2.interaction_run_stop()


    def ovens_wdt(self):
        if self.ui.ovens_wdt.isChecked():
            self.wdt.wdt_switch('Ovens','ON')
        else:
            self.wdt.wdt_switch('Ovens','OFF')
    def power_wdt(self):
        if self.ui.power_wdt.isChecked():
            self.wdt.wdt_switch('Power', 'ON')
        else:
            self.wdt.wdt_switch('Power','OFF')
    def jdsu_wdt(self):
        if self.ui.jdsu_wdt.isChecked():
            self.wdt.wdt_switch('JDSU', 'ON')
        else:
            self.wdt.wdt_switch('JDSU', 'OFF')
    def imb1_wdt(self):
        if self.ui.imb1_wdt.isChecked():
            self.wdt.wdt_switch('IMB1', 'ON')
        else:
            self.wdt.wdt_switch('IMB1', 'OFF')
    def imb2_wdt(self):
        if self.ui.imb2_wdt.isChecked():
            self.wdt.wdt_switch('IMB2', 'ON')
        else:
            self.wdt.wdt_switch('IMB2', 'OFF')
    def lc1_wdt(self):
        if self.ui.lc1_wdt.isChecked():
            self.wdt.wdt_switch('LC1', 'ON')
        else:
            self.wdt.wdt_switch('LC1', 'OFF')
    def lc2_wdt(self):
        if self.ui.lc2_wdt.isChecked():
            self.wdt.wdt_switch('LC2', 'ON')
        else:
            self.wdt.wdt_switch('LC2', 'OFF')





