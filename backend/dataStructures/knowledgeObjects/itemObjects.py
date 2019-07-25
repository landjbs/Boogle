class Thing():
    """ Top-level class for generic, non-creation objects """
    def __init__(self, name):
        self.name = name
        self.description = None
        self.relatedItems = None

    def set_description(self, description):
        self.description = description

    def add_relatedItem(self, item):
        if self.relatedItems:
            self.relatedItems.append(item)
        else:
            self.relatedItems = [item]


class Food(Item):
    def __init__(self, name):
        Item.__init__(self, name)
        self.calories = None
        self.recipieList = None

    def set_calories(self, calories):
        self.calories = calories

    def add_recipie(self, recipie):
        if self.recipieList:
            self.recipieList.append(recipie)
        else:
            self.recipieList = [recipie]


class Institution(Item):
    """
    Items with locations and lists of associated people like sports teams
    and universities
    """
    def __init__(self, name):
        Item.__init__(self, name)
        self.people = None
        self.location = None

    def set_location(self, location):
        self.location = location

    def add_person(self, person):
        if self.people:
            self.people.append(person)
        else:
            self.people = [person]
