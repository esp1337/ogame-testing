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
        
    def sendWarning(self, body, title="Error Warning!"):
        self.mailer.sendEmail(title, body)
        
    def printFlightInfo(self, detailedFlightList):
        print "Current Fleet Info :: "
        for flight in detailedFlightList:
            print "\t" + flight.toShortString()
    
if __name__ == '__main__':
    try:
        wl = weblogic.Weblogic()
        ld = wl.login()
        timer = TimedExpeditions()
        hostileCount = header.Header()
        
        loop = expedition_loop.ExpeditionLoop(wl, ld)
        #expeditionTime = 2700
        enemyFlights = 0
        while True:
            enemyFlights = hostileCount.flights(wl, ld)
            if int(enemyFlights) > 0:
                print str(enemyFlights) + " incoming hostile flight(s)!"
                timer.sendWarning(enemyFlights)
            #if expeditionTime >= 2700:
            #    print "Taking 2700 seconds off of expedition time & sending expeditions!"
            #    loop.runExpeditions(wl, ld)
            #    expeditionTime -= 2700
            if loop.checkOpenSlots():
                loop.runExpeditions(wl, ld)
                
            detailed = hostileCount.detailedFlights(wl, ld)
            timer.printFlightInfo(detailed)
            timer.delayTime(450, 900)
    except:
        info = "Unexpected error"
        print info
        timer.sendWarning(info)
        raise
