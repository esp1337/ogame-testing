#import re
import weblogic
import header
import time
import random
import expedition_loop
import mail

class TimedExpeditions:
    
    def __init__(self):
        self.mailer = mail.MailSender()
    
    def delayTime(self, lowerBound, upperBound):
        delay = random.randint(lowerBound, upperBound)
        print "Sleeping " + str(delay) + " seconds..."
        time.sleep(delay)
        return delay
    
    def sendWarning(self, flightCount):
        title = "Attack warning!"
        body = str(flightCount) + " hostile fleets are incoming!"
        self.mailer.sendEmail(title, body)
    
if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    timer = TimedExpeditions()
    hostileCount = header.Header()
    
    loop = expedition_loop.ExpeditionLoop(wl, ld)
    expeditionTime = 2700
    enemyFlights = 0
    while True:
        enemyFlights = hostileCount.flights(wl, ld)
        print str(enemyFlights)
        if int(enemyFlights) > 0:
            print str(enemyFlights) + " incoming hostile flight(s)!"
            timer.sendWarning(enemyFlights)
        if expeditionTime >= 2700:
            print "Taking 2700 seconds off of expedition time & sending expeditions!"
            loop.runExpeditions(wl, ld)
            expeditionTime -= 2700
        expeditionTime += timer.delayTime(450, 900)