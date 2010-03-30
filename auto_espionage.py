import weblogic
import planets
import galaxy

class Espionage:
    
    def __init__(self):
        pass
    
if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    scanner = galaxy.GalaxyScanner()
    planetManager = planets.PlanetManager(wl)
    planetList = planets.PlanetManager.availablePlanets(planetManager, wl.getRecentResponse())
    planetList.append(planetManager.currentPlanet(wl.getRecentResponse()))
    targetPlanet = ""
    for planet in planetList:
        print planet.name
        if str(planet.name) == targetPlanet:
            planet.switch("overview",ld.session)
            loc = planet.location
            scanner.scanSystems(wl, ld, loc.galaxy, loc.solarsystem, 20)