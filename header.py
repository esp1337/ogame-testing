import re
import weblogic

class Header:
    
    def __init__(self):
        self.HOSTILE_INDEX = re.compile(r"\"hostile\":([0-9]*)")
        
    def flights(self, wl, ld):
        header_url = "http://%s.ogame.org/game/index.php?page=fetchEventbox&session=%s&ajax=1" %\
                    (wl.server, ld.session)
        page = wl.fetchResponse(header_url)
        enemy = self.HOSTILE_INDEX.search(page.getvalue()).group(1)
        return enemy

if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    h = Header()
    enemy = h.flights(wl, ld)
    print "Number of hostile flights:"+str(enemy)