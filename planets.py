"""
OGAME LULZ
Planet logic module

elliot 2010
"""

import weblogic

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
        self.PLANET_COUNT_REGEX = re.compile(r"countColonies.*?n\>(d)")
        # group1: id;  group2: usedfields; group3: totalfields; group4: name; group5: coords
        self.PLANET_FIND_REGEX = re.compile(r"smallplanet.*?ref\=\".*?cp\=(.*?)\".*?km\s\((d+)\/(d+).*?name=\"\>(.*?)\<\/span.*?koords\"\>(.*?)\<\/")

    def countPlanets(self, page):
        """
        Count the number of planets

        args: page - the source of the page from which to find the planet info
        """
        planetcount = self.PLANET_COUNT_REGEX.search(page.getvalue()).group(1)
        return planetcount

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
                
        aps = self.PLANET_FIND_REGEX.finditer()
        for ap in aps:
            p = Planet(self.wl, ap.group(4), ap.group(1),
                       ap.group(2), ap.group(3),
                       (Location(ap.group(5))))
            planets.append(p)
            # if we don't know about this planet, add it to the self.planets list
            if p.id not in existing_ids:
                self.planets.append(p)
            
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
        koords_match = re.search("\[(d+)\:(d+)\:(d+)\]", koords_string)
        self.galaxy = koords_match.group(1)
        self.solarsystem = koords_match.group(2)
        self.slot = koords_match.group(3)

    def timeSinceActive(self):
        """
        find time since this location was active
        """
        pass
