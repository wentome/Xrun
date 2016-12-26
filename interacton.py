from frigate import Frigate
from radiogram import Radiogram
from telnetlib import Telnet
import re

class Interaction(Frigate,Radiogram):
    def __init__(self,parent):
        self.parent=parent
        Frigate.__init__(self, parent)
        Radiogram.__init__(self, parent)
        # Radiogram.set_destination(self,'message/') #defult destination is ''message/''
        self.fd = Telnet()
        self.address = ''

    def interaction_run_start(self, address):
        self.address = address
        self.run_start(self.parent)
        print '%s open %s' % (self.parent, self.address)

    def interaction_run_stop(self):
        self.run_stop()
        print '%s stop'%(self.parent)

    def run_init(self):
        self.interaction_open()
        print'%s connect'%(self.parent)

    def run_process_hs(self):
        recv_message = self.scan_message()

        if recv_message.find(':') >= 0:
            com_type = recv_message.split(':', 1)[0]
            com_string = recv_message.split(':', 1)[1]

            if com_type.find('sys') >= 0:
                self.conf_log(com_string)
                self.response_message('%s sys' % self.parent)

            if com_type.find('st') >= 0:
                self.sequence_transmission(com_string)
                self.response_message('%s st' % self.parent)
            if com_type.find('ft') >= 0:
                self.response_message(self.filter_transmission(com_string))

    def run_process(self):
        # print'imb process '   rir1c
        res = self.fd.read_very_eager()  # just test conncet
        self.record_log(res)
        self.feed_dog()

    def run_except(self):
        print '%s expect' % self.parent
        self.interaction_close()
        self.interaction_open()

    def run_end(self):
        self.interaction_close()
        print '%s end' % self.parent

    def interaction_open(self):
        address = self.address.split(':', 1)  # IP :PORT
        self.fd.open(address[0], int(address[1]), 1)

    def interaction_close(self):
        self.fd.close()



    def sequence_transmission(self,com):
        com_list = com.split('|')
        #print com_list
        for com_i in com_list:
            self.fd.write(str(com_i.split('@@')[0]))
            try:
                time=int(com_i.split('@@')[2])
            except:
                res=self.fd.read_until(com_i.split('@@')[1], 1)
            else:
                res=self.fd.read_until(com_i.split('@@')[1], time)
            self.record_log(res)


    def filter_transmission(self,com):
        com_list = com.split('|')
        self.fd.write(str(com_list[0].split('@@')[0]))
        try:
            time = int(com_list[0].split('@@')[2])
        except:
            res=self.fd.read_until(com_list[0].split('@@')[1], 1)
        else:
            #print time
            res=self.fd.read_until(com_list[0].split('@@')[1], time)
        self.record_log(res)
        re_string=com_list[1]
        print re_string
        re_res=re.match(r'\d', res)

        if re_res:
            return re_res
        else:
            return 'miss'












