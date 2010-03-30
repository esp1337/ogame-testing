import weblogic
import header
import time
import random
import smallCargoRaid
import mail
import planets
import messages
import galaxy

class AutoAttacks:
    
    def __init__(self):
        self.mailer = mail.MailSender()
    
    def delayTime(self, lowerBound=2, upperBound=5):
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
    aa = AutoAttacks()
    
    try:
        wl = weblogic.Weblogic()
        ld = wl.login()
        print "PLANET FINDER"
        planetManager = planets.PlanetManager(wl)
        planetList = planets.PlanetManager.availablePlanets(planetManager, wl.getRecentResponse())
        planetList.append(planetManager.currentPlanet(wl.getRecentResponse()))
        targetPlanet = ""
        spiedFrom = None
        
        print "GALAXY SCANNER"
        scanner = galaxy.GalaxyScanner()
        for planet in planetList:
            print planet.name
            if str(planet.name) == targetPlanet:
                spiedFrom = planet
                planet.switch("overview", ld.session)
                loc = planet.location
                scanner.scanSystems(wl, ld, loc.galaxy, loc.solarsystem, 20)
                break
        
        print "MESSAGE PARSER"
        msgs = messages.Messages(wl, ld)
        eInfo = msgs.getUnreadMessages()
        
        print "AUTO ATTACKER"
        attacker = smallCargoRaid.SCAttacker(wl, ld)
        for info in eInfo:
            sc = info.getNumSC()
            home_gal = spiedFrom.location.galaxy
            home_ss = spiedFrom.location.solarsystem
            home_posn = spiedFrom.location.slot
            tgt_gal = info.gal
            tgt_ss = info.ss
            tgt_posn = info.slot
            attacker.attackFlightFromPlanet(sc, home_gal, home_ss, home_posn, tgt_gal, tgt_ss, tgt_posn)
            aa.delayTime(1, 3)
    except:
        info = "Unexpected error "
        print info
        #aa.sendWarning(info)
        raise
