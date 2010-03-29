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
        
        espInfo = []
        
        msgListPageURL = self.getEspionageListURL(page, 7)
        msgListPage = wl.fetchResponse(msgListPageURL).getvalue()
        self.delayTime()
        
        unreadMessageResult = self.unreadMessageREGEX.findall(msgListPage)
        for result in unreadMessageResult:
            messageURL = self.messagePage %\
                    (self.wl.server, result)
            message = wl.fetchResponse(messageURL).getvalue()
            self.delayTime(1,2)
            
            if self.hasNoDefense(message) and self.hasNoFleet(message):
                print "Valid target!"
                result = self.loc_resREGEX.search(message)
                info = EspionageInfo(result.group(1), result.group(2), result.group(3), result.group(4), result.group(5), result.group(6))
                if info.getNumSC() > 1:
                    print espInfo.getLocation()
                    espInfo.append(info)
        return espInfo
    
    def hasNoFleet(self, message):
        fleetTable = 0
        tables = self.infoTablesREGEX.findall(message)
        fleet = tables[fleetTable]
        fleetList = self.tableKeyValueREGEX.findall(fleet)
        print fleetList
        if len(fleetList) < 1:
            print "No fleet!"
            return True
        return False
    
    def hasNoDefense(self, message):
        defenseTable = 1
        tables = self.infoTablesREGEX.findall(message)
        defense = tables[defenseTable]
        defenseList = self.tableKeyValueREGEX.findall(defense)
        print defenseList
        if len(defenseList) < 1:
            print "No defense!"
            return True
        firstItem = defenseList[0]
        if firstItem == None:
            print "No defense!"
            return True
        elif str(firstItem[0]) == "Anti-Ballistic Missiles":
            print "No defense!"
            return True
        return False

class EspionageInfo:

    def __init__(self, gal, ss, slot, met, cry, deut):
        self.gal = gal
        self.ss = ss
        self.slot = slot
        self.met = met
        self.cry = cry
        self.deut = deut
        
    def getNumSC(self):
        total = self.getTotalResWorth()
        sc = total / 5000
        sc += 1
        return int(sc)
    
    def getTotalResWorth(self):
        total = float(0)
        total += float(self.met)
        total += float(self.cry) * 2
        total += float(self.deut) * 3
        return total
    
    def getLocation(self):
        return "["+str(self.gal)+":"+str(self.ss)+":"+str(self.slot)+"]"

if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    msgs = Messages(wl, ld)
    info = msgs.getUnreadMessages()
    print str(info.sort(lambda x,y: y.getNumSC() - x.getNumSC()))
    for eInfo in info:
        print eInfo.getLocation()
        print eInfo.getTotalResWorth()
        print eInfo.getNumSC()
    
    