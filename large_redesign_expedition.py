#import re
import weblogic
import re

class LargeExpedition:
    
    def __init__(self, wl, ld):
        self.wl = wl
        self.ld = ld
        self.fleet1 = "http://%s.ogame.org/game/index.php?page=fleet1&session=%s"
        self.fleet2 = "http://%s.ogame.org/game/index.php?page=fleet2&session=%s"
        self.fleet2argsz = "&galaxy=%s&system=%s&position=%s&type=1&mission=0&speed=10&am204=&am205=110&am206=&am207=&am215=&am211=&am213=2&am202=&am203=80&am209=&am210=1"
        self.fleet3 = "http://%s.ogame.org/game/index.php?page=fleet3&session=%s"
        self.fleet3argsz = "&type=1&mission=0&union=0&am203=80&am205=110&am213=2&am210=1&galaxy=%s&system=%s&position=16&speed=10"
        self.flights = "http://%s.ogame.org/game/index.php?page=movement&session=%s"
        self.flightargsz = "&holdingtime=1&expeditiontime=1&galaxy=%s&system=%s&position=16&type=1&mission=15&union2=0&holdingOrExpTime=1&speed=10&am203=80&am205=110&am213=2&am210=1&resource1=0&resource2=0&resource3=0"

        self.lcCountREGEX = re.compile(r"title=\"\|Large Cargo \(([0-9]+)\)\"")
        self.probeCountREGEX = re.compile(r"title=\"\|Espionage Probe \(([0-9]+)\)\"")
        self.destroyerCountREGEX = re.compile(r"title=\"\|Destroyer \(([0-9]+)\)\"")
        self.hfCountREGEX = re.compile(r"title=\"\|Heavy Fighter \(([0-9]+)\)\"")
        
        self.impossibleDispatchREGEX = re.compile(r"Fleet dispatch impossible")
        self.fleetSlotREGEX = re.compile(r"<span>fleets:</span> ([0-9]+)/([0-9]+)")
        self.expSlotREGEX = re.compile(r"<span>Expeditions:</span> ([0-9]+)/([0-9]+)") 
        
    def expeditionFlightFromPlanet(self, gal, ss, posn):
        fleet_url = self.fleet1 %\
                    (self.wl.server, self.ld.session)
        page = self.wl.fetchResponse(fleet_url)
        if not self.checkForShips(page):
            return False
        if not self.checkForSlots(page):
            return False
        
        second_page = self.fleet2+self.fleet2argsz
        fleet_url = second_page %\
                    (self.wl.server, self.ld.session, gal, ss, posn)
        print fleet_url
        page = self.wl.fetchResponse(fleet_url)

        third_page = self.fleet3+self.fleet3argsz
        fleet_url = third_page %\
                    (self.wl.server, self.ld.session, gal, ss)
        print fleet_url
        page = self.wl.fetchResponse(fleet_url)
        
        final_page = self.flights+self.flightargsz
        fleet_url = final_page %\
                    (self.wl.server, self.ld.session, gal, ss)
        print fleet_url
        page = self.wl.fetchResponse(fleet_url)
        return True
        
    def checkForShips(self, fleet1page):
        ret = False
        
        impossible = self.impossibleDispatchREGEX.search(fleet1page.getvalue())
        if impossible != None:
            print "No ships on planet!"
            return ret
        else:
            probes = self.probeCountREGEX.search(fleet1page.getvalue()).group(1)
            if probes == None:
                print "No probes matched!"
                return ret
            destroyers = self.destroyerCountREGEX.search(fleet1page.getvalue()).group(1)
            if destroyers == None:
                print "No destroyers matched!"
                return ret
            hf = self.hfCountREGEX.search(fleet1page.getvalue()).group(1)
            if hf == None:
                print "No heavy fighters matched!"
                return ret
            lc = self.lcCountREGEX.search(fleet1page.getvalue()).group(1)
            if lc == None:
                print "No large cargoes matched!"
                return ret
            
            print "Probes :: " + probes
            print "Destroyers :: " + destroyers
            print "Heavy Fighters :: " + hf
            print "Large Cargoes :: " + lc
            
            if int(probes) >= 1 and int(hf) >= 110 and int(lc) >= 80 and int(destroyers) >= 2:
                ret = True
            return ret
    
    def checkForSlots(self, fleet1page):
        ret = False
        
        fleetMatch = self.fleetSlotREGEX.search(fleet1page.getvalue())
        fleetCurrent = fleetMatch.group(1)
        fleetTotal = fleetMatch.group(2)
        print "Fleet :: " + fleetCurrent + "/" + fleetTotal
         
        expMatch = self.expSlotREGEX.search(fleet1page.getvalue())
        expCurrent = expMatch.group(1)
        expTotal = expMatch.group(2)
        print "Expeditions :: " + expCurrent + "/" + expTotal
        
        if int(fleetCurrent)+1 < int(fleetTotal) and int(expCurrent) < int(expTotal):
            ret = True
        else:
            print "No fleetslots available!"
        return ret
    
if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    f = LargeExpedition(wl, ld)
    f.expeditionFlight()
    