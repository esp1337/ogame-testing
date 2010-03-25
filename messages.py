import weblogic
import re
import time
import random

class Messages:
    
    def __init__(self, wl, ld):
        self.wl = wl
        self.ld = ld
        self.messageListPage = "http://%s.ogame.org/game/index.php?page=messages&session=%s&displayCategory=%s&displayPage=%s&siteType=undefined&ajax=1 "
        self.unreadMessageREGEX = re.compile("(?:<tr class=\"entry trigger new\" id=\"\w+\">.+?href=\"(index.php\?.+?)\">)+", re.DOTALL)
        
        self.messagePage = "http://%s.ogame.org/game/%s"
        self.loc_resREGEX = re.compile("\[(\d+):(\d+):(\d+)\].+?Metal:\s*</td>\s*<td>\s*([\d.]+).+?Crystal:\s*</td>\s*<td>\s*([\d.]+).+?Deuterium:\s*</td>\s*<td>\s*([\d.]+)", re.DOTALL)
        self.infoTablesREGEX = re.compile("class=\"fleetdefbuildings spy\">(.+?)</table>", re.DOTALL)
        self.tableKeyValueREGEX = re.compile("<td class=key>(.+?)</td>\s*<td class=value>([\d.]+)</td>", re.DOTALL)
        
    def delayTime(self, min=1, max=5):
        delay = random.randint(min,max)
        print "Sleeping " + str(delay) + " seconds between requests..."
        time.sleep(delay)
        
    def getEspionageListURL(self, page=1, cat = 7):
        spyUrl = self.messageListPage %\
                    (self.wl.server, self.ld.session, str(cat), str(page))
        return spyUrl
    
    def getSpecificMessage(self, args):
        msgUrl = self.messagePage %\
                    (self.wl.server, args)
        return msgUrl
    
    def getUnreadMessages(self):
        page = 1
        
        msgListPageURL = self.getEspionageListURL(page, 7)
        msgListPage = wl.fetchResponse(msgListPageURL).getvalue()
        self.delayTime()
        
        unreadMessageResult = self.unreadMessageREGEX.findall(msgListPage)
        for result in unreadMessageResult:
            print result
            messageURL = self.messagePage %\
                    (self.wl.server, result)
            print messageURL
            message = wl.fetchResponse(messageURL).getvalue()
            self.delayTime(1,2)
            result = self.loc_resREGEX.search(message)
            print "[" + str(result.group(1)) + ":" + str(result.group(2)) + ":" + str(result.group(3)) +"]"
        
if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    msgs = Messages(wl, ld)
    msgs.getUnreadMessages()
    
    