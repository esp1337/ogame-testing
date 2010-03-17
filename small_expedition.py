#import re
import weblogic

class SmallExpedition:
    
    def __init__(self, wl, ld):
        self.wl = wl
        self.ld = ld
        self.fleet1 = "http://%s.ogame.org/game/index.php?page=fleet1&session=%s"
        self.fleet2 = "http://%s.ogame.org/game/index.php?page=fleet2&session=%s"
        self.fleet2args = "&galaxy=3&system=361&position=5&type=1&mission=0&speed=10&am204=&am205=&am206=&am207=&am215=&am211=&am213=&am202=1&am203=&am209=&am210=1"
        self.fleet3 = "http://%s.ogame.org/game/index.php?page=fleet3&session=%s"
        self.fleet3args = "&type=1&mission=0&union=0&am202=1&am210=1&galaxy=3&system=361&position=16&speed=10"
        self.flights = "http://%s.ogame.org/game/index.php?page=movement&session=%s"
        self.flightargs = "&holdingtime=1&expeditiontime=1&galaxy=3&system=361&position=16&type=1&mission=15&union2=0&holdingOrExpTime=1&speed=10&am202=1&am210=1&resource1=0&resource2=0&resource3=0"
#        self.HOSTILE_INDEX = re.compile(r"\"hostile\":([0-9]*)")
        
    def expeditionFlight(self):
        #self.wl = weblogic.Weblogic()
        #ld = self.wl.login()
        fleet_url = self.fleet1 %\
                    (self.wl.server, self.ld.session)
        page = self.wl.fetchResponse(fleet_url)
        print page.getvalue()
        
        second_page = self.fleet2+self.fleet2args
        print second_page
        print ld.session
        print self.wl.server
        fleet_url = second_page %\
                    (self.wl.server, self.ld.session)
        page = self.wl.fetchResponse(fleet_url)
        print page.getvalue()

        third_page = self.fleet3+self.fleet3args
        fleet_url = third_page %\
                    (self.wl.server, self.ld.session)
        page = self.wl.fetchResponse(fleet_url)
        print page.getvalue()
        
        final_page = self.flights+self.flightargs
        fleet_url = final_page %\
                    (self.wl.server, self.ld.session)
        page = self.wl.fetchResponse(fleet_url)
        print page.getvalue()
        
if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    f = SmallExpedition(wl, ld)
    f.expeditionFlight()
    