import weblogic
import re
import smtplib
import httplib
import urllib2

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
        
    def getEspionageListURL(self, page=1, cat = 7):
        spyUrl = self.messageListPage %\
                    (self.wl.server, self.ld.session, str(cat), str(page))
        return spyUrl
    
    def getSpecificMessage(self, args):
        msgUrl = self.messagePage %\
                    (self.wl.server, args)
        return msgUrl
    
    def getUnreadMessages(self, page=1):
        espInfo = []
        
        msgListPageURL = self.getEspionageListURL(page, 7)
        try:
            msgListPage = self.wl.fetchResponse(msgListPageURL).getvalue()
        except (smtplib.SMTPConnectError, httplib.BadStatusLine):
            msgListPage = self.wl.fetchResponse(msgListPageURL).getvalue()
        
        unreadMessageResult = self.unreadMessageREGEX.findall(msgListPage)
        newMessages = len(unreadMessageResult)
        print "Parsing " + str(newMessages) + " new espionage reports!"
        for result in unreadMessageResult:
            messageURL = self.messagePage %\
                    (self.wl.server, result)
            try:
                message = self.wl.fetchResponse(messageURL).getvalue()
            except (smtplib.SMTPConnectError, httplib.BadStatusLine, urllib2.HTTPError):
                message = self.wl.fetchResponse(messageURL).getvalue()
            
            if self.hasNoDefense(message) and self.hasNoFleet(message):
                print "Valid target!"
                result = self.loc_resREGEX.search(message)
                info = EspionageInfo(result.group(1), result.group(2), result.group(3), result.group(4), result.group(5), result.group(6))
                print "SC needed :: " + str(info.getNumSC())
                if info.getNumSC() >= 16:
                    print info.getLocation()
                    espInfo.append(info)
                    
        if newMessages == 50:
            page += 1
            print "50 messages parsed, checking page " + str(page) + " for more."
            moreMessages = self.getUnreadMessages(page)
            espInfo.extend(moreMessages)
        
        espInfo.sort(self.compareByTotalRes)
        return espInfo
    
    def compareByTotalRes(self, info1, info2):
        res1 = info1.getTotalResWorth()
        res2 = info2.getTotalResWorth()
        if res1 > res2:
            return -1
        elif res2 > res1:
            return 1
        else:
            return 0
    
    def hasNoFleet(self, message):
        fleetTable = 0
        tables = self.infoTablesREGEX.findall(message)
        try:
            fleet = tables[fleetTable]
        except IndexError:
            return False
        fleetList = self.tableKeyValueREGEX.findall(fleet)
        print fleetList
        if len(fleetList) < 1:
            print "No fleet!"
            return True
        return False
    
    def hasNoDefense(self, message):
        defenseTable = 1
        tables = self.infoTablesREGEX.findall(message)
        try:
            defense = tables[defenseTable]
        except IndexError:
            return False
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
        self.met = self.getFloatFromString(met)
        self.cry = self.getFloatFromString(cry)
        self.deut = self.getFloatFromString(deut)
        print self.getLocation()+"\t"+str(self.getTotalResWorth())+"\t"+str(self.getNumSC())
        
    def getNumSC(self):
        total = self.met + self.cry + self.deut
        totalCapture = total / 2
        sc = totalCapture / 5000
        sc += 1
        return int(sc)
    
    def getTotalResWorth(self):
        total = float(0)
        total += float(self.met)
        total += float(self.cry) * 2
        total += float(self.deut) * 3
        return total
    
    def getFloatFromString(self, target):
        digitRegex = re.compile("(\d+)")
        delimeterRegex = re.compile("\.")
        
        count = len(delimeterRegex.findall(target))
        number = digitRegex.search(target).group(1)
        
        if int(count) > 0:
            value = int(number) * (1000 ** int(count))
        else:
            value = number
        
        return float(value)
    
    def getLocation(self):
        return "["+str(self.gal)+":"+str(self.ss)+":"+str(self.slot)+"]"
    
if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    msgs = Messages(wl, ld)
    eInfo = msgs.getUnreadMessages()
    for info in eInfo:
        print info.getLocation()+"\t"+str(info.getTotalResWorth())+"\t"+str(info.getNumSC())
    
    
