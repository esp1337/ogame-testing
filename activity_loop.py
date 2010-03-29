#import re
import weblogic
import header
import time
import random
import mail
import planets

class ActivityLoop:
    
    def __init__(self):
        self.mailer = mail.MailSender()
        self.overview = "http://%s.ogame.org/game/index.php?page=overview&session=%s"
    
    def delayTime(self, lowerBound=1, upperBound=5):
        delay = random.randint(lowerBound, upperBound)
        print "Sleeping " + str(delay) + " seconds..."
        time.sleep(delay)
        return delay
    
    def sendAttackWarning(self, flightCount):
        title = "Attack warning!"
        body = str(flightCount) + " hostile fleets are incoming!"
        self.mailer.sendEmail(title, body)
        
    def sendErrorWarning(self, body, title="Error Warning!"):
        self.mailer.sendEmail(title, body)
        
    def printFlightInfo(self, detailedFlightList):
        print "Current Fleet Info :: "
        for flight in detailedFlightList:
            print "\t" + flight.toShortString()
    
if __name__ == '__main__':
    try:
        wl = weblogic.Weblogic()
        ld = wl.login()
        timer = ActivityLoop()
        hostileCount = header.Header()
        
        planetManager = planets.PlanetManager(wl)
        timer.delayTime()
        fleetUrl = timer.overview %\
                    (wl.server, ld.session)
        fleetpage = wl.fetchResponse(fleetUrl)
        planetList = planets.PlanetManager.availablePlanets(planetManager, fleetpage)
        
        enemyFlights = 0
        while True:
            enemyFlights = hostileCount.flights(wl, ld)
            if int(enemyFlights) > 0:
                print str(enemyFlights) + " incoming hostile flight(s)!"
                timer.sendAttackWarning(enemyFlights)
                
            
            
            for planet in planetList:
                print "Switching to planet :: " + str(planet.name)
                planet.switch("overview", ld.session)
                
            detailed = hostileCount.detailedFlights(wl, ld)
            timer.printFlightInfo(detailed)
            timer.delayTime(450, 900)
    except:
        info = "Unexpected error"
        print info
        timer.sendErrorWarning(info)
        raise