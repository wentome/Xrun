import  json
import os
import time


class Radiogram:
    def __init__(self,parent,destination='message/'):
        self.parent=parent
        self.message = { 'target': '', 'source': self.parent, 'sync':0, 'message':''}
        self.destination=destination

    def set_destination(self,destination):
        self.destination = destination

    def send_message(self,target,message):
        self.message['target']=target
        self.message['message'] = message
        try:
            fc = open(self.destination+target+'_'+self.parent+'.json', 'w')
            json.dump(self.message, fc)
            fc.close()
        except:
            return 'send filed'
        else:
            self.message['sync']+=1
            for i in range(20):
                time.sleep(0.2)
                try:
                    fc = open(self.destination + target + '_' + self.parent + '.json', 'r')
                    message_res = json.load(fc)
                    fc.close()
                except:
                    if i==4:
                        return 'no response'
                else:
                    if message_res['target']==self.parent and message_res['sync']==self.message['sync']:
                        return message_res['message']
            return 'time out'

    def scan_message(self):
        for filename in os.listdir(self.destination):
            if filename.find(self.parent) >= 0:
                try:
                    fc = open(self.destination+filename, 'r')
                    message_res = json.load(fc)
                    fc.close()
                except:
                    return 'read IDLE'
                else:
                    if message_res['target']==self.parent:
                        self.message['target'] = message_res['source']
                        self.message['source']=self.parent
                        self.message['sync']= message_res['sync']+1
                        return  message_res['message']
                    else:
                        continue
        return 'NO message'

    def response_message(self,message):
        self.message['message'] = message
        fc = open(self.destination + self.parent+'_'+self.message['target'] + '.json', 'w')
        json.dump(self.message, fc)
        fc.close()


    def query(self):
        print 'query'



    def report(self):
        print 'report'

