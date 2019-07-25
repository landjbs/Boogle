from dataStructures.knowledgeObjects.thingObjects import Thing

class Person(Thing):
    def __init__(self, name):
        """ People only need a name to be initialized """
        Thing.__init__(self, name)
        self.birthDate = None
        self.deathDate = None
        self.profession = None
        self.relationships = None

    def set_birthDate(self, birthDate):
        self.birthDate = birthDate

    def set_deathDate(self, deathDate):
        self.deathDate = deathDate

    def set_profesison(self, profession):
        self.profession = profession

    def add_relationships(self, person, relationship):
        """ All relationships members are also people objects """
        if self.relationships:
            self.relationships.update({relationship:person})
        else:
            self.relationships = {relationship:person}


class Creative(Person):
    def __init__(self, name):
        Person.__init__(self, name)
        self.works = None

    def add_work(self, work):
        if self.works:
            self.works.append(work)
        else:
            self.works = [work]

class Athelete(Person):
    def __init__(self, name):
        Person.__init__(self, name)
        self.team = None

    def set_team(self, team):
        self.team = team


class Politician(Person):
    def ___init__(self, name):
        """ Politician() wraps Person() with no initial changes """
        Person.__init__(self, name)
        self.region = None

    def set_region(self, region):
        self.region = None


class Academic(Person):
    def __init__(self, name):
        """ Academic() wraps Person() with no initial changes """
        Person.__init__(self, name)
        self.field = None
        self.publications = None

    def set_field(self, field):
        self.field = field

    def add_publication(self, publication):
        """ publications are types of 'creations' """
        if self.publications:
            self.publications.append(publication)
        else:
            self.publications = [publication]
