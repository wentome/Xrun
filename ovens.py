from frigate import Frigate
from radiogram import Radiogram
from telnetlib import Telnet

class Ovens(Frigate,Radiogram):
    def __init__(self):
        Frigate.__init__(self, 'Ovens')
        Radiogram.__init__(self, 'Ovens')
        #Radiogram.set_destination(self,'message/') #defult destination is ''message/''
        self.fd = Telnet()
        self.address = ''


    def run_init(self):
        self.ovens_open()
    def run_process_hs(self):

        recv_message= self.scan_message()

        if recv_message.find('get temp')>=0:
            temp=self.get_temp().split(',',3)
            self.response_message('temp is %s'%(temp[0]))

        elif recv_message.find('set temp')>=0:
            self.response_message('set temp %s ok!'%(recv_message.split(':',1)[1]))

    def run_process(self):
        #print 'ovens run_process'
        res= self.get_temp()
        temp=res.split(',',3)
        self.cia.data['Ovens']['real_temp'] = temp[0]
        self.cia.data['Ovens']['set_temp'] = temp[1]
        self.cia.data['Ovens']['WDT']=3
    def run_except(self):
        self.ovens_close()
        self.ovens_open()
    def run_end(self):
        try:
            self.ovens_close()
        except:
            pass
        print 'end'

    def ovens_run_start(self,address='10.220.52.40:10004'):
        self.address=address
        self.run_start('Ovens')

    def ovens_run_stop(self):
        self.run_stop()

    def ovens_open(self):
        address = self.address.split(':', 1) #IP :PORT

        self.fd.open(address[0], int(address[1]), 1)

    def ovens_close(self):
        self.fd.close()

    def power_on(self):
        self.fd.write("POWER,ON\n")
        return self.fd.read_some()

    def power_off(self):
        self.fd.write("POWER,OFF\n")
        return self.fd.read_some()

    def set_temp(self, value):
        self.fd.write("TEMP,S" + str(value) + "\n")
        return self.fd.read_some()

    def get_temp(self):
        self.fd.write("temp?\n")
        return self.fd.read_some()