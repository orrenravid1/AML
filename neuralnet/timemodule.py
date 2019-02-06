import time

class Clock:
    def __init__(self):
        self.prevtime = 0
        self.currtime = 0
    def start(self):
        self.prevtime = 0
        self.currtime = 0
    def tick(self,ms):
        self.prevtime = self.currtime
        self.currtime += ms
    def deltatime(self):
        return self.currtime-self.prevtime
    def get_time(self):
        return self.currtime
        
    #add this if intending to use realtime
    '''
    def get_true_time():
        return time.clock()
    '''
