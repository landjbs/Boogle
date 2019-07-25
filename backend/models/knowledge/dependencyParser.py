import spacy

# Load the large English NLP model
nlp = spacy.load('en_core_web_lg')

# The text we want to examine
text = """London is the capital and most populous city of England and
the United Kingdom.  Standing on the River Thames in the south east
of the island of Great Britain, London has been a major settlement
for two millennia. It was founded by the Romans, who named it Londinium.
"""

def get_entities(text):
    doc = nlp(text)
    return [(entity.text, entity.label_) for entity in doc.ents]
