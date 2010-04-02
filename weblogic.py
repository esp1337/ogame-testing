"""
OGAME LULZ
Weblogic Module

elliot 2010
"""

import time
import random
import re
import unittest
import urllib
import urllib2
import threading
import Queue
import StringIO

class Weblogic:
    """
    This class handles the web logic for the OGame bot/shell/thing.
    Methods here interface directly with the code on the website and return
    results which can be used by systems of higher intelligence.
    """

    def __init__(self):
        self.requestQueue = Queue.Queue()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        self.lastFetchedURL = None
        f = open("login.ogame")
        info = f.read()
        self.user = re.search("user:\s(.*?);", info, re.M).group(1)
        self.passwd = re.search("password:\s(.*?);", info, re.M).group(1)
        self.server = re.search("server:\s(.*?);", info, re.M).group(1)
        self.SESSION_REGEX = re.compile(r"[0-9A-Fa-f]{12}")
        self.PLAYER_REGEX = re.compile("id=\"playerName\".*?efy\"\>(.*?)\<", re.S|re.M)
        self.session = None

        headers = [('Keep-Alive', "300")]
        self.opener.addheaders = headers

    def delayTime(self, lowerBound=2, upperBound=4):
        delay = random.randint(lowerBound, upperBound)
        print "Sleeping " + str(delay) + " seconds after request..."
        time.sleep(delay)
        return delay

    def submitRequest(self, request):
        self.requestQueue.put(request)

    def setRecentResponse(self, response):
        self._recentResponse = response
        
    def getRecentResponse(self):
        return self._recentResponse

    def fetchResponse(self, request):

        if isinstance(request, str):
            request = urllib2.Request(request)
        if self.lastFetchedURL:
            request.add_header('Referer', self.lastFetchedURL)

        response = self.opener.open(request)
        self.lastFetchedURL = response.geturl()
        cachedResponse = StringIO.StringIO(response.read())
        cachedResponse.seek(0)
        self.setRecentResponse(cachedResponse)
        self.delayTime()
        return cachedResponse
    
    def login(self):
        login_url = "http://%s.ogame.org/game/reg/login2.php?uni_url=%s.ogame.org&login=%s&pass=%s" %\
                    (self.server, self.server, self.user, self.passwd)
        page = self.fetchResponse(login_url)
        session = self.SESSION_REGEX.search(page.getvalue()).group(0)
        player = self.PLAYER_REGEX.search(page.getvalue()).group(1)
        ld = LoginData(session, player)
        return ld

class RequestService(threading.Thread):
    """
    The requestService is a thread that runs and waits for requests to put into
    the request queue. When requests are added to the queue, the requestService
    is notified and will process them.
    """

    def __init__(self):
        pass

class LoginData:
    """
    Store relevant login data in this class.
    """

    def __init__(self, session, player):
        self.session = session
        self.player = player


#####################################
#        TESTS
#####################################

class LoginSetup(unittest.TestCase):
    def setUp(self):
        self.wl = Weblogic()
        self.ld = self.wl.login()

class LoginFileTest(LoginSetup):
    def testWeHaveSessionID(self):
        self.failIfEqual(None, self.ld.session)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginFileTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

