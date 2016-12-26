from frigate import Frigate
from radiogram import Radiogram
from telnetlib import Telnet
import re
import time
class JDSU(Frigate,Radiogram):
    def __init__(self):
        Frigate.__init__(self, 'JDSU')
        Radiogram.__init__(self, 'JDSU')
        self.fd = Telnet()
        #Radiogram.set_destination(self,'message/') #defult destination is ''message/''
        self.address=''

    def run_init(self):
        self.jdsu_open()
    def run_process_hs(self):
        #print 'jdsu hs'

        recv_message= self.scan_message()

        if recv_message.find(':') >= 0:
            com_type = recv_message.split(':', 1)[0]
            com_string = recv_message.split(':', 1)[1]

            if com_type.find('sys') >= 0:
                if com_type.find('sys') >= 0:
                    self.conf_log(com_string)
                    self.response_message('%s sys' % self.parent)

            if com_type.find('st') >= 0:
                if com_string.find('get_tx') >= 0:
                    tx = self.get_tx()
                    #self.record_log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'  tx:'+ tx+'\r\n')
                    self.response_message('tx:%s' % (tx))
                elif com_string.find('get_error') >= 0:
                    error = self.get_error()
                    #self.record_log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  error:' + error + '\r\n')
                    self.response_message('error:%s' % (error))




    def run_process(self):
        #print 'jdsu run_process'
        self.cia.data['JDSU']['sync'] = self.get_sync()
        self.cia.data['JDSU']['laser'] = self.get_laser()
        self.cia.data['JDSU']['test'] = self.get_test()
        self.cia.data['JDSU']['tx'] = self.get_tx()
        self.cia.data['JDSU']['bit_error'] = self.get_error()
        self.cia.data['JDSU']['WDT']=3
    def run_except(self):
        self.jdsu_close()
        self.jdsu_open()
    def run_end(self):
        try:
            self.jdsu_close()
        except:
            pass
        print 'end'

    def jdsu_run_start(self,address='10.220.52.74'):
        self.address=address
        self.run_start('JDSU')

    def jdsu_run_stop(self):
        self.run_stop()


    def jdsu_open(self):
        self.fd.open(self.address, '23', 1)
        self.fd.read_until("Telnet+>")
        self.step_tpshell()

    def jdsu_close(self):
        #self.quit_tpshell()
        self.fd.close()



    def step_in_telnet(self):
        self.fd.write("\n")
        return self.fd.read_until("Telnet+>")
    def step_tpshell(self):
        self.fd.write("tpshell\n")
        return self.fd.read_until("tp:>")

    def quit_tpshell(self):
        self.fd.write("quit\n")
        return self.fd.read_until("Telnet+>")


    def tp_shell_command(self, command):
        self.fd.write(command)
        res=self.fd.read_until("tp:>", 1)
        self.record_log(res)
        return res


    def jdsu_laser(self, state='ON'):
        if state == 'ON':
            self.tp_shell_command("set carrier/txlaser on\n")
        elif state == 'OFF':
            self.tp_shell_command("set carrier/txlaser off\n")

    def jdsu_test(self, state='ON'):
            if state == 'ON':
                self.tp_shell_command("set test/test start\n")
            elif state == 'OFF':
                self.tp_shell_command("set test/test stop\n")

    def get_tx(self):
        res = self.tp_shell_command("payload/rx/byte_count\n")
        temp_list = re.findall(r"\d+\.?\d*", res)
        return  temp_list[0]
    def get_error(self):
        res = self.tp_shell_command("payload/rx/biterrors\n")
        temp_list = re.findall(r"\d+\.?\d*", res)
        return  temp_list[0]
    def get_sync(self):
        res = self.tp_shell_command("payload/rx/sync\n")
        if res.find("lost") >= 0:
            return 'lost'
        elif res.find("found") >= 0:
            return 'found'
        elif res.find("hist") >= 0:
            return 'hist'
    def get_laser(self):
        if self.tp_shell_command("get carrier/txlaser \n").find("on") >= 0:
            return 'ON'
        else:
            return 'OFF'

    def get_test(self):
        if self.tp_shell_command("get test/test \n").find("start") >= 0:
            return 'ON'
        else:
            return 'OFF'


