"""
OGAME LULZ
Weblogic Module

elliot 2010
"""

import re
import unittest
import urllib
import urllib2
import threading
import StringIO

class Weblogic:
    """
    This class handles the web logic for the OGame bot/shell/thing.
    Methods here interface directly with the code on the website and return
    results which can be used by systems of higher intelligence.
    """

    def __init__(self):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        self.lastFetchedURL = None
        f = open("login.ogame")
        info = f.read()
        self.user = re.search("user:\s(.*?);", info, re.M).group(1)
        self.passwd = re.search("password:\s(.*?);", info, re.M).group(1)
        self.server = re.search("server:\s(.*?);", info, re.M).group(1)
        self.SESSION_REGEX = re.compile(r"[0-9A-Fa-f]{12}")
        self.PLAYER_REGEX = re.compile(r"id=\"playerName\".*?efy\"\>(.*?)\<")
        self.session = None

    def fetchResponse(self, request):

        if isinstance(request, str):
            request = urllib2.Request(request)
        if self.lastFetchedURL:
            request.add_header('Referer', self.lastFetchedURL)

        response = self.opener.open(request)
        self.lastFetchedURL = response.geturl()
        cachedResponse = StringIO.StringIO(response.read())
        cachedResponse.seek(0)
        return cachedResponse
    
    def login(self):
        login_url = "http://%s.ogame.org/game/reg/login2.php?uni_url=%s.ogame.org&login=%s&pass=%s" %\
                         (self.server, self.server, self.user, self.passwd)
        page = self.fetchResponse(login_url)
        self.session = self.SESSION_REGEX.search(page.getvalue()).group(0)
        self.player = self.PLAYER_REGEX.search(page.getvalue()).group(1)

class LoginData:
    """
    Store relevant login data in this class.
    """

    def __init__(self, session):
        self.session = session


#####################################
#        TESTS
#####################################

class LoginSetup(unittest.TestCase):
    def setUp(self):
        self.wl = Weblogic()
        self.wl.login()

class LoginFileTest(LoginSetup):
    def testWeHaveSessionID(self):
        self.failIfEqual(None, self.wl.session)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginFileTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

