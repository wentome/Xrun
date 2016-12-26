from frigate import Cia
import time
import threading
import winsound
class WDT():
    def __init__(self,member):
        self.members = member
        for menber in self.members:
            exec ('self.' + menber.lower() + '_wdt_active=False')
            exec('self.' + menber.lower() + '_wdt_die=False')
        self.start_wdt_thread()

    def wdt_switch(self,member='',flag=''):
        try:
            if flag=='ON':
                exec ('self.' + member.lower() + '_wdt_active=True')
            elif flag=='OFF':
                exec ('self.' + member.lower() + '_wdt_active=False')
        except:
            print 'no %s WDT'%(member)



    def wdt(self):
        while 1:
            wdt_alarm = 0
            time.sleep(3)
            for menber in self.members:
                if eval('self.'+menber.lower()+'_wdt_active'):
                    Cia.data[menber]['WDT'] -= 1
                    if Cia.data[menber]['WDT'] <= 0:
                        print '%s died'%(menber)
                        exec ('self.' + menber.lower() + '_wdt_die=True')
                        wdt_alarm+=1
                    else:
                        exec ('self.' + menber.lower() + '_wdt_die=False')
            if wdt_alarm>0:
                winsound.Beep(500,1000)


    def start_wdt_thread(self):
        threads = threading.enumerate()
        thread_not_start = True
        for m in threads:
            if str(m).find('WDT') != -1:
                thread_not_start = False
                break
        if thread_not_start:
            T = threading.Thread(target=self.wdt, name='WDT')
            T.isAlive()
            T.setDaemon(True)
            T.start()
            #print "WDT start..."
        else:
            print "WDT have started"

