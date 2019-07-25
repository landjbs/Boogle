class Creation():
    """ Top-level class to define artistic and academic creations by humans """
    def __init__(self, title):
        self.title = title
        self.creationDate = None
        self.rating = None
        self.description = None
        self.relatedWorks = None

    def set_creationDate(self, creationDate):
        self.creationDate = creationDate

    def set_rating(self, rating):
        self.rating = rating

    def set_description(self, description):
        self.description = description

    def add_relatedWork(self, relatedWork):
        """ Currently unordered list of related objects, soon to be ordered """
        if self.relatedWorks:
            self.relatedWorks.append(relatedWork)
        else:
            self.relatedWorks = [relatedWork]


class Movie(Creation):
    def __init__(self, title):
        Creation.__init__(self, title)
        self.cast = None

    def add_castMember(self, castMember):
        """
        Cast members are people objects; currently in list by dict mapping
        to role could be cool
        """
        if self.cast:
            self.cast.append(castMember)
        else:
            self.cast = [castMember]

class WrittenWork(Creation):
    def __init__(self, title):
        Creation.__init__(self, title)
        self.authors = None

    def add_author(self, author):
        if self.authors:
            self.authors.append(author)
        else:
            self.authors = [author]
