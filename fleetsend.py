import re
import unittest
import urllib
import urllib2
import threading
import StringIO
import weblogic

class Fleetsend:

    def __init__(self):
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        self.lastFetchedURL = None
        f = open("login.ogame")
        info = f.read()
        self.user = re.search("user:\s(.*?);", info, re.M).group(1)
        self.passwd = re.search("password:\s(.*?);", info, re.M).group(1)
        self.server = re.search("server:\s(.*?);", info, re.M).group(1)
        self.SESSION_REGEX = re.compile(r"[0-9A-Fa-f]{12}")
        self.session = None