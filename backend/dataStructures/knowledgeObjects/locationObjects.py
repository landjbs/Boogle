class Location():
    def __init__(self, name):
        """ Locations only need a name to be initialized """
        self.name = name
        self.coordinates = None
        self.factsList = None
        self.relatedLocations = None

    def set_coordinates(self, longitude, latitude):
        """ coordinates are a tuple of (longitude, latitude) """
        self.coordinates = (longitude, latitude)

    def add_fact(self, fact):
        if self.factsList:
            self.factsList.append(fact)
        else:
            self.factsList = [fact]

    def add_relatedLocation(self, relatedLocation):
        """ Currently unranked list of related locations """
        if self.relatedLocations:
            self.relatedLocations.append(relatedLocation)
        else:
            self.relatedLocations = [relatedLocation]


class City(Location):
    def __init__(self, name):
        Location.__init__(self, name)
        self.population = None
        self.foundationDate = None
        self.country = None

    def set_population(self, population):
        self.population = population

    def set_foundationDate(self, foundationDate):
        self.foundationDate = foundationDate

    def set_country(self, country):
        self.country = country


class Country(Location):
    def __init__(self, name):
        Location.__init__(self, name)
        self.population = None
        self.foundationDate = None
        self.gdp = None
        self.religion = None
        self.cities = None
        self.area = None

    def set_population(self, population):
        self.population = population

    def set_foundationDate(self, foundationDate):
        self.foundationDate = foundationDate

    def set_gdp(self, gdp):
        self.gdp = gdp

    def set_religion(self, religion):
        self.religion = religion

    def add_city(self, city):
        if self.cities:
            self.cities.append(city)
        else:
            self.cities = [city]

    def set_area(self, area):
        self.area = area
