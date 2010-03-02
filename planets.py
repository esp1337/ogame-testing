"""
OGAME LULZ
Planet logic module

elliot 2010
"""

import weblogic
import unittest
import re

class PlanetManager:
    """
    Manage information about planets
    """

    def __init__(self, wl):
        """
        initialize a planet manager

        args: wl - Weblogic instance
        """
        self.planets = []
        self.wl = wl
        self.PLANET_COUNT_REGEX = re.compile("span\>(\d+)\/\d+\<", re.S|re.M)
        # group1: id;  group2: usedfields; group3: totalfields; group4: name; group5: coords
        self.PLANET_FIND_REGEX = re.compile("smallplanet.*?href\=\".*?cp\=(.*?)\".*?km\s\((\d+)\/(\d+).*?name\"\>(.*?)\<\/span.*?koords\"\>(.*?)\<\/", re.S|re.M)

    def countPlanets(self, page):
        """
        Count the number of planets

        args: page - the source of the page from which to find the planet info
        """
        if not isinstance(page, str):
            page = page.getvalue()
        m = self.PLANET_COUNT_REGEX.search(page)
        planetcount = m.group(1)
#        planetcount = self.PLANET_COUNT_REGEX.search(page).group(1)
        return int(planetcount)

    def availablePlanets(self, page):
        """
        Find all planets for this login and create Planet objects for each
        of them.

        return: a list of Planet objects
        args: page - the source of the page from which to find the planet info
        """
        # make a list of ids for planets we know about
        existing_ids = []
        for pl in self.planets:
            existing_ids.append(pl.id)

        planets = []

        if not isinstance(page, str):
            page = page.getvalue()
        aps = self.PLANET_FIND_REGEX.finditer(page)
        for ap in aps:
            p = Planet(self.wl, ap.group(4), ap.group(1),
                       int(ap.group(2)), int(ap.group(3)),
                       (Location(ap.group(5))))
            planets.append(p)
            # if we don't know about this planet, add it to the self.planets list
            if p.id not in existing_ids:
                self.planets.append(p)
        return planets
            
class Planet:
    """
    Store information about a planet

    FIELDS:
    wl: Weblogic instance
    name: string
    id: string
    location: Location instance
    """

    def __init__(self, weblogic, name, planet_id,
                 usedfields, totalfields,
                 location):
        self.wl = weblogic
        self.name = name
        self.id = planet_id
        self.usedfields = usedfields
        self.totalfields = totalfields
        self.location = location

    def switch(self, pane):
        """
        post a request to switch to this planet
        
        args: pane - is a string describing which pane to switch to.,
           ie, shipyard, resources, etc.
        """
        sw_url = "http://%s.ogame.org/game/index.php?page=%s&session=%s&cp=%s" \
                 % (self.wl.server, pane, self.session, self.id)
        self.wl.fetchResponse(sw_url)

    def toString(self):
        return "name: %s\nfields: %s/%s\nlocation: %s" %\
              (self.name, str(self.usedfields), str(self.totalfields), (self.location.toString()))

class Location:
    """
    Represents a set of coordinates
    """

    def __init__(self, coords_string):
        """
        Take a coords string in the form of

            [galaxy:solarsystem:slot]

        where galaxy, solarsystem, and slot are representative integers
        """
        self.string = coords_string
        koords_match = re.search("\[(\d+)\:(\d+)\:(\d+)\]", coords_string)
        if (koords_match != None):
            self.galaxy = koords_match.group(1)
            self.solarsystem = koords_match.group(2)
            self.slot = koords_match.group(3)
        else:
            print "LOCATION INSTANTIATION FAIL"

    def timeSinceActive(self):
        """
        find time since this location was active
        """
        pass
    
    def toString(self):
        print self.string

#####################################
#        TESTS
#####################################

class LoginSetup(unittest.TestCase):
    def setUp(self):
        print "running setup"
        self.wl = weblogic.Weblogic()
        f = open("fakeresponse.txt")
        self.fakeResponse = f.read()

        self.pmgr = PlanetManager(self.wl)
        f.close()

class PlanetTest(LoginSetup):

    def testPlanetCount(self):
        self.assertEqual(3, (self.pmgr.countPlanets(self.fakeResponse)))

    def testPlanetFindRegex(self):
        m = self.pmgr.PLANET_FIND_REGEX.search(self.fakeResponse)
        self.assertNotEqual(None, m)
        
    def testPlanetAllocation(self):
        planets = self.pmgr.availablePlanets(self.fakeResponse)
        self.assertEqual(2, len(planets))
        turtwig = False
        for planet in planets:
            lulz = planet.toString()
            print lulz
            if planet.name == 'turtwig':
                turtwig = True
                break
        self.assertEqual(True, turtwig)
#        self.assertEqual(163, planets[0].totalfields)
        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PlanetTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
