import re
import weblogic
import planets
import time
import random
"""
check probe/flight status
"""
class GalaxyScanner:
    
    def __init__(self):
        self.SLOT_REGEX = re.compile("(?:<tr class=\"row\">(.+?)</tr>)+", re.DOTALL)
        self.POSITION_REGEX = re.compile("<td class=\"position\">(\d+)</td>", re.DOTALL)
        self.INACTIVE_REGEX = re.compile("<span class=\"status_abbr_(?:long)?inactive\">(.+?)</span>", re.DOTALL)
        self.VACA_REGEX = re.compile("<span class=\'status_abbr_vacation")
        self.NOOB_REGEX = re.compile("<span class=\'status_abbr_noob")
        self.BAN_REGEX = re.compile("<span class=\'status_abbr_banned")
        
        self.galaxyURL = "http://%s.ogame.org/game/index.php?page=galaxyContent&session=%s&ajax=1&galaxy=%s&system=%s"
        self.espionageSendURL = "http://%s.ogame.org/game/index.php?page=minifleet&session=%s&ajax=1&mission=6&galaxy=%s&system=%s&position=%s&type=1&shipCount=5"
        
    def getAttackableInactivePlanetsInSystem(self, wl, ld, gal, system):
        galaxy_url = self.galaxyURL %\
                    (wl.server, ld.session, gal, system)
        page = wl.fetchResponse(galaxy_url)
        page = page.getvalue()
        
        return self.getAttackableInactivePlanets(page, gal, system)
        
    def getAttackableInactivePlanets(self, page, gal, system):
        planets = []
        slots = self.SLOT_REGEX.findall(page)
        for slot in slots:
            posn = self.POSITION_REGEX.search(slot).group(1)
            inactive = self.INACTIVE_REGEX.search(slot)
            vmode = self.VACA_REGEX.search(slot)
            noob = self.NOOB_REGEX.search(slot)
            ban = self.BAN_REGEX.search(slot)
            if inactive != None and vmode == None and ban == None and noob == None:
                planet = PlanetInfo(gal, system, posn)
                planets.append(planet)
        return planets
    
    def sendProbes(self, wl, ld, gal, system, slot):
        probe_url = self.espionageSendURL %\
                    (wl.server, ld.session, str(gal), str(system), str(slot))
        print probe_url
        page = wl.fetchResponse(probe_url)
        page = page.getvalue()
        #returns a string with
        #statusCode totalSlots probesLeft recyclersLeft ipmsLeft probesSent missionType [coords]
        print page
    
    def scanSystems(self, wl, ld, gal_start, system_start, scanLimit):
        print "Starting up/down scan of systems with a limit of " + str(scanLimit)
        self.scanUpSystems(wl, ld, gal_start, system_start, scanLimit)
        self.scanDownSystems(wl, ld, gal_start, system_start, scanLimit)
        
    def scanDownSystems(self, wl, ld, gal_start, system_start, scanLimit):
        gal = gal_start
        system = int(system_start)
        systemOffset = int(0)
        while systemOffset <= int(scanLimit):
            system -= 1
            systemOffset += 1
            planets = self.getAttackableInactivePlanetsInSystem(wl, ld, gal, system)
            self.delayTime(3, 6)
            for planet in planets:
                print "Probing planet " + planet.getInfoString()
                self.sendProbes(wl, ld, gal, system, planet.slot)
                self.delayTime(2, 5)
            
    
    def scanUpSystems(self, wl, ld, gal_start, system_start, scanLimit):
        gal = gal_start
        system = int(system_start)
        systemOffset = int(0)
        while systemOffset <= int(scanLimit):
            system += 1
            systemOffset += 1
            planets = self.getAttackableInactivePlanetsInSystem(wl, ld, gal, system)
            self.delayTime(3, 6)
            for planet in planets:
                print "Probing planet " + planet.getInfoString()
                self.sendProbes(wl, ld, gal, system, planet.slot)
                self.delayTime(2, 5)
            

    def delayTime(self, lowerBound, upperBound):
        delay = random.randint(lowerBound, upperBound)
        print "Sleeping " + str(delay) + " seconds..."
        time.sleep(delay)
        return delay

class PlanetInfo:
    def __init__(self, gal, system, slot):
        self.galaxy = gal
        self.system = system
        self.slot = slot
        
    def getInfoString(self):
        return "%s:%s:%s" %\
                    (str(self.galaxy), str(self.system), str(self.slot))
        
if __name__ == '__main__':
    if 1==0:
        f = open("galaxy_source_test.html")
        info = f.read()
        hdr = GalaxyScanner()
        planets = hdr.getAttackableInactivePlanets(info, 5, 357)
        for planet in planets:
            print planet.getInfoString()
    else:
        wl = weblogic.Weblogic()
        ld = wl.login()
        scanner = GalaxyScanner()
        scanner.scanSystems(wl, ld, 3, 361, 25)
