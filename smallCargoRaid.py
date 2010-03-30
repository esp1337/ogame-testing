import weblogic
import planets
import re

class SCAttacker:
    
    def __init__(self, wl, ld):
        self.wl = wl
        self.ld = ld
        self.fleet1 = "http://%s.ogame.org/game/index.php?page=fleet1&session=%s"
        self.fleet2 = "http://%s.ogame.org/game/index.php?page=fleet2&session=%s"
        self.fleet2argsz = "&galaxy=%s&system=%s&position=%s&type=1&mission=1&speed=10&am205=&am206=&am207=&am215=&am211=&am202=%s&am203=&am208=&am209=&am210="
        self.fleetCheck = "http://%s.ogame.org/game/index.php?page=fleetcheck&session=%s&ajax=1&espionage="
        self.fleetCheckargsz = "&galaxy=%s&system=%s&planet=%s&type=1"
        self.fleet3 = "http://%s.ogame.org/game/index.php?page=fleet3&session=%s"
        self.fleet3argsz = "&type=1&mission=1&union=0&am202=%s&galaxy=%s&system=%s&position=%s&speed=10"
        self.flights = "http://%s.ogame.org/game/index.php?page=movement&session=%s"
        self.flightargsz = "&holdingtime=1&expeditiontime=1&galaxy=%s&system=%s&position=%s&type=1&mission=1&union2=0&holdingOrExpTime=0&speed=10&am202=%s&resource1=0&resource2=0&resource3=0"

        self.probeCountREGEX = re.compile(r"title=\"\|Espionage Probe \(([0-9]+)\)\"")
        self.scCountREGEX = re.compile(r"title=\"\|Small Cargo \(([0-9]+)\)\"")
        self.impossibleDispatchREGEX = re.compile(r"Fleet dispatch impossible")
        self.fleetSlotREGEX = re.compile(r"<span>fleets:</span> ([0-9]+)/([0-9]+)")
        self.expSlotREGEX = re.compile(r"<span>Expeditions:</span> ([0-9]+)/([0-9]+)") 
        
    def attackFlightFromPlanet(self, shipCount, home_gal, home_ss, home_posn, tgt_gal, tgt_ss, tgt_posn):
        fleet_url = self.fleet1 %\
                    (self.wl.server, self.ld.session)
        page = self.wl.fetchResponse(fleet_url)
        if not self.checkForShips(page, shipCount):
            return False
        if not self.checkForSlots(page):
            return False
        
        second_page = self.fleet2+self.fleet2argsz
        fleet_url = second_page %\
                    (self.wl.server, self.ld.session, home_gal, home_ss, home_posn, str(shipCount))
        page = self.wl.fetchResponse(fleet_url)

        check_page = self.fleetCheck+self.fleetCheckargsz
        fleet_url = check_page %\
                    (self.wl.server, self.ld.session, tgt_gal, tgt_ss, tgt_posn)
        page = self.wl.fetchResponse(fleet_url)
        if not page.getvalue() == str(0):
            print "Fleetcheck returned a nonzero value:" + str(page.getvalue())
            return False
        

        third_page = self.fleet3+self.fleet3argsz
        fleet_url = third_page %\
                    (self.wl.server, self.ld.session, str(shipCount), tgt_gal, tgt_ss, tgt_posn)
        page = self.wl.fetchResponse(fleet_url)
        
        final_page = self.flights+self.flightargsz
        fleet_url = final_page %\
                    (self.wl.server, self.ld.session, tgt_gal, tgt_ss, tgt_posn, str(shipCount))
        page = self.wl.fetchResponse(fleet_url)
        return True
        
    def checkForShips(self, fleet1page, shipCount = 0):
        ret = False
        
        impossible = self.impossibleDispatchREGEX.search(fleet1page.getvalue())
        if impossible != None:
            print "No ships on planet!"
            return ret
        else:
            sc = self.scCountREGEX.search(fleet1page.getvalue()).group(1)
            if sc == None:
                print "No sc matched!"
                return ret
            print "SC :: " + sc
            
            if int(sc) > shipCount:
                ret = True
            return ret
    
    def checkForSlots(self, fleet1page):
        ret = False
        
        fleetMatch = self.fleetSlotREGEX.search(fleet1page.getvalue())
        fleetCurrent = fleetMatch.group(1)
        fleetTotal = fleetMatch.group(2)
        print "Fleet :: " + fleetCurrent + "/" + fleetTotal
         
        if int(fleetCurrent)+1 < int(fleetTotal):
            ret = True
        else:
            print "No fleetslots available!"
        return ret
    
if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    
    planetManager = planets.PlanetManager(wl)
    planetList = planets.PlanetManager.availablePlanets(planetManager, wl.getRecentResponse())
    planetList.append(planetManager.currentPlanet(wl.getRecentResponse()))
    targetPlanet = ""#"planetName"
    spiedFrom = None
    
    attacker = SCAttacker(wl, ld)
    for planet in planetList:
        print planet.name
        if str(planet.name) == targetPlanet:
            spiedFrom = planet
            planet.switch("overview", ld.session)

            sc = 1
            home_gal = spiedFrom.location.galaxy
            home_ss = spiedFrom.location.solarsystem
            home_posn = spiedFrom.location.slot
            tgt_gal = ""#info.gal
            tgt_ss = ""#info.ss
            tgt_posn = ""#info.slot
            flew = attacker.attackFlightFromPlanet(sc, home_gal, home_ss, home_posn, tgt_gal, tgt_ss, tgt_posn)
            if not flew:
                print "Attack failed!"
                break
            break
