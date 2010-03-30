import re

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
    
class RunningTime:
    def __init__(self):
        pass
    
    def customCompare(self, info1, info2):
        res1 = info1.getTotalResWorth()
        res2 = info2.getTotalResWorth()
        if res1 > res2:
            return -1
        elif res2 > res1:
            return 1
        else:
            return 0
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
    
if __name__ == '__main__':
    run = RunningTime()
    
    run.getFloatFromString("50")
    run.getFloatFromString("50.000")
    run.getFloatFromString("50..")
    
    espInfo = []
    
    espInfo.append(EspionageInfo(1, 1, 1, 500, 50, 4))
    espInfo.append(EspionageInfo(2, 2, 2, 500, 50, 5))
    espInfo.append(EspionageInfo(3, 3, 3, 500, 50, 3))
    
    for info in espInfo:
        #print info.getLocation()+"\t"+str(info.getTotalResWorth())+"\t"+str(info.getNumSC())
        pass
    
    #print "Sorting!"
    espInfo.sort(run.customCompare)
    
    for info in espInfo:
        #print info.getLocation()+"\t"+str(info.getTotalResWorth())+"\t"+str(info.getNumSC())
        pass
    
    reg = re.compile("(\w)(\w)")
    target = "abcdefgh"
    results = reg.findall(target)
    #print results
    #print len(results)
    for res in results:
        #print res[0]
        pass