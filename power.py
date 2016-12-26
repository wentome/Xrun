from frigate import Frigate
from radiogram import Radiogram
import socket

class Power(Frigate,Radiogram):
    def __init__(self):
        Frigate.__init__(self,'Power') #init Frigate
        Radiogram.__init__(self, 'Power')
        self.address=''
    def run_init(self):
        self.pow_open()
    def run_process_hs(self):
        #print  'power hs'
        recv_message = self.scan_message()

        if recv_message.find('get vol') >= 0:
            vol=self.get_voltage()
            self.response_message('vol is %s'%(vol))

        elif recv_message.find('get cur') >= 0:
            cur=self.get_current()
            self.response_message('cur is %s'%(cur))


    def run_process(self):
        #print 'power run_process '
        self.cia.data['Power']['vol'] = self.get_voltage()
        self.cia.data['Power']['cur'] = self.get_current()
        self.cia.data['Power']['WDT']=3
    def run_except(self):
        self.pow_close()
        self. pow_open()
    def run_end(self):
        try:
            self.pow_close()
        except:
            pass
        print 'end'

    def power_run_start(self, address='10.220.52.111'):
        self.address = address
        self.run_start('Power')

    def power_run_stop(self):
        self.run_stop()

    def pow_open(self):
        host =self.address
        self.s = socket.socket()
        self.s.settimeout(0.3)
        self.s.connect((host, 2268))

    def pow_close(self):
        self.s.close()

    def get_dev_info(self):
        self.sendCmd("*IDN?\n")
        return self.s.recv(256)

    def get_voltage(self):
        self.s.send("MEASure:VOLTage?\n")
        return self.s.recv(256)

    def get_current(self):
        self.s.send("MEASure:CURRent?\n")
        return self.s.recv(256)
