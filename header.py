import re
import weblogic

class Header:
    
    def __init__(self):
        self.HOSTILE_INDEX = re.compile(r"\"hostile\":([0-9]*)")
        
    def flights(self):
        self.wl = weblogic.Weblogic()
        ld = self.wl.login()
        header_url = "http://%s.ogame.org/game/index.php?page=fetchEventbox&session=%s&ajax=1" %\
                    (self.wl.server, ld.session)
        page = self.wl.fetchResponse(header_url)
        enemy = self.HOSTILE_INDEX.search(page.getvalue()).group(1)
        return enemy

if __name__ == '__main__':
    h = Header()
    enemy = h.flights()
    print enemy