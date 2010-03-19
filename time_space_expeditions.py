#import re
import weblogic
import time
import expedition_loop

class TimedExpeditions:
    pass
    
if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    loop = expedition_loop.ExpeditionLoop(wl, ld)
    while True:
        loop.runExpeditions(wl, ld)
        time.sleep(2700)