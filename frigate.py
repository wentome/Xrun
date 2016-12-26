import time
import threading
import collections


class Cia:
    data = collections.defaultdict(dict)
########################
#    run_star
#   [run_init]
#   [run_process_hs]
#   [run_process]
#   [run_expect]
#   [run_end]
#    run_stop
##########################

class Frigate:
    def __init__(self, parent):
        self.parent = parent
        self.cia=Cia()
        self.cia.data[self.parent]={'state': 0, 'WDT': 3}
        self.running = False
        self.time_expect = 0.5
        self.time_process_interval = 0.2
        self.times = 5
        self.counter = self.times

        self.log_flag = False
        self.log_name = './log/%s.log' % parent
    def conf_log(self,com_string):
        if com_string.find('EN_log') >= 0:
            try:
                self.log_name = com_string.split('@@')[1] + '.log'
            except:
                pass
            self.log_flag = True
        if com_string.find('UN_log') >= 0:
            self.log_flag = False
            self.log_name = './log/%s.log' % self.parent

    def record_log(self,string):
        if self.log_flag:
            if len(string)>0:
                fd=open(self.log_name,'ab+')
                fd.write(string)
                fd.close()

    def feed_dog(self,dog_food=3):
        self.cia.data[self.parent]['WDT'] = dog_food
##################################################################

    def run_init(self):
        print 'run init'

    def run_process_hs(self):
        print 'run_process_hs'

    def run_process(self):
        print 'run_process'

    def run_except(self):
        print 'run_except'

    def run_end(self):
        print 'run end'

#################################################################

    def run(self):
        while 1:
            try:
               self.run_init()
            except:
                print '%s init failed'%(self.parent)
                if not self.running:
                    break
                time.sleep(self.time_expect)
            else:
                break
        while 1:
            if not self.running:
                break
            try:
                if self.counter==0:
                    self.counter=self.times
                    self.run_process_hs()
                    self.run_process()
                else:
                    self.counter-=1
                    self.run_process_hs()
            except:
                while 1:
                    try:
                        self.run_except()
                    except:
                        print '%s process error'%(self.parent)
                        if not self.running:
                            break
                        time.sleep(self.time_expect)
                    else:
                        break
            else:
                time.sleep(self.time_process_interval)

        self.run_end()


    #################################################################

    def run_start(self, name):
        threads = threading.enumerate()
        thread_not_start = True
        for m in threads:
            if str(m).find(name) != -1:
                thread_not_start = False
                break
        self.running=True
        if thread_not_start:
            T = threading.Thread(target=self.run, name=name)
            T.isAlive()
            T.setDaemon(True)
            T.start()
            #print "%s start..."%(name)
        else:
            print "%s have started"%(name)
    ##################################################################
    def run_stop(self, flag=False):
        self.running = flag


