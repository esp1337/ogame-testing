#import re
import weblogic
import planets
import time
import random
import small_expedition
import large_redesign_expedition

class ExpeditionLoop:
    
    def __init__(self, wl, ld):
        self.wl = wl
        self.ld = ld
    
    def smallExpeditionFromPlanet(self, planet):
        planet.switch("overview", self.ld.session);
        gal = planet.location.galaxy
        ss = planet.location.solarsystem
        posn = planet.location.slot
        print gal + ":" + ss + ":" + posn
        f = small_expedition.SmallExpedition(self.wl, self.ld)
        return f.expeditionFlightFromPlanet(gal, ss, posn)
    
    def largeExpeditionFromPlanet(self, planet):
        planet.switch("overview", self.ld.session);
        gal = planet.location.galaxy
        ss = planet.location.solarsystem
        posn = planet.location.slot
        print gal + ":" + ss + ":" + posn
        f = large_redesign_expedition.LargeExpedition(self.wl, self.ld)
        return f.expeditionFlightFromPlanet(gal, ss, posn)
    
    def delayTime(self):
        delay = random.randint(1,5)
        print "Sleeping " + str(delay) + " seconds..."
        time.sleep(delay)
        
if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    loop = ExpeditionLoop(wl, ld)
    loginpage = wl._recentResponse
    planetManager = planets.PlanetManager(wl)
    loop.delayTime()
    planetList = planets.PlanetManager.availablePlanets(planetManager, loginpage)
    
    for planet in planetList:
        loop.delayTime()
        loop.largeExpeditionFromPlanet(planet)
    
    for planet in planetList:
        loop.delayTime()
        loop.smallExpeditionFromPlanet(planet)
    