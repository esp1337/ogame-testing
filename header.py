import re
import weblogic

class Header:
    
    def __init__(self):
        self.flightListings = "http://%s.ogame.org/game/index.php?page=eventList&session=%s&ajax=1&height=500&width=690"
        self.flightInfoURL = "http://%s.ogame.org/game/index.php?page=fetchEventbox&session=%s&ajax=1"
        #find a hostile count
        self.HOSTILE_INDEX = re.compile(r"\"hostile\":([0-9]*)")
        #find the info for each separate flight
        self.FLIGHTS_REGEX = re.compile("<div class=\"eventFleet\" id=\"eventRow-[\d]+\">(.+?)</div>",re.DOTALL)
        #find particular fields in flight info
        self.DETAILED_FLIGHT_REGEX = re.compile("arrivalTime\">([0-9]+):([0-9]+):([0-9]+).+?descFleet\">([\w ]+)<.+?missionFleet\">.+?<span>([\w \)\(]+)<.+?originFleet\">(.+?)</li>.+?coordsOrigin\">.+?\[(\d+):(\d+):(\d+).+?detailsFleet\">\s+([\d\.]+).+?destFleet\">([\w ]+)<.+?destCoords\">.+\[(\d+):(\d+):(\d+)\]",re.DOTALL)
        
    def flights(self, wl, ld):
        header_url = self.flightInfoURL %\
                    (wl.server, ld.session)
        page = wl.fetchResponse(header_url)
        matches = self.HOSTILE_INDEX.search(page.getvalue())
        if matches is None:
            enemy = 0
        else:
            enemy = matches.group(1)
        return enemy
    
    def detailedFlights(self, wl, ld):
        header_url = self.flightListings %\
                    (wl.server, ld.session)
        print header_url
        page = wl.fetchResponse(header_url)
        page = page.getvalue()
        
        return self.detailedFlightsOnPage(page)
    
    def detailedFlightsOnPage(self, page):
        allflights = []
        flights = self.FLIGHTS_REGEX.findall(page)
        for flight in flights:
            info = self.DETAILED_FLIGHT_REGEX.findall(flight)
            if info.__len__() > 0:
                info = info.pop()
                f = FlightInfo(info[0],info[1],info[2],info[3],info[4],info[5],info[6],
                           info[7],info[8],info[9],info[10],info[11],info[12],info[13])
                allflights.append(f)
        return allflights

class FlightInfo:
    """
    Store information about a flight

    FIELDS:
    arrival hour
    arrival minute
    arrival second
    fleet descr
    fleet mission
    fleet origin (name)
    origin gal
    origin system
    origin slot
    fleet details (count, doesn't go into the shiplink)
    fleet destination (name)
    dest gal
    dest system
    dest slot
    """

    def __init__(self, incHour, incMin, incSec, descrip, mission, incOrigin, incGal, incSys, incSlot, incDetails, tgtName, tgtGal, tgtSys, tgtSlot):
        #fix hour for GMT
        self.arrival_hour=str(int(incHour)-6)
        if int(self.arrival_hour) < 0:
            self.arrival_hour = int(self.arrival_hour) + 24
        self.arrival_minute=incMin
        self.arrival_second=incSec
        self.fleet_descr=descrip
        self.fleet_mission=mission
        self.fleet_origin=incOrigin# (name)
        self.origin_gal=incGal
        self.origin_system=incSys
        self.origin_slot=incSlot
        self.fleet_details=incDetails# (count, doesn't go into the shiplink for ship breakdown)
        self.fleet_destination=tgtName# (name)
        self.dest_gal=tgtGal
        self.dest_system=tgtSys
        self.dest_slot=tgtSlot

    def toShortString(self):
        return "%s ships from %s to %s to do a(n) %s %s arriving on %s:%s:%s" %\
              (str(self.fleet_details), str(self.fleet_origin), str(self.fleet_destination), str(self.fleet_descr), str(self.fleet_mission), str(self.arrival_hour), str(self.arrival_minute), str(self.arrival_second))

if __name__ == '__main__':
    if 0==1:
        f = open("flights_infotest.html")
        info = f.read()
        hdr = Header()
        flights = hdr.detailedFlightsOnPage(info)
        for flight in flights:
            print flight.toShortString()
    else:
        wl = weblogic.Weblogic()
        ld = wl.login()
        h = Header()
        enemy = h.flights(wl, ld)
        print "Number of hostile flights:"+str(enemy)
        details = h.detailedFlights(wl, ld)
        if details.__len__() > 0:
            first = details[0]
            print first.toShortString()
