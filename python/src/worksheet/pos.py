from enum import Enum


class POS(Enum):
    Noun = 0  # Blue
    Verb = 1  # Green
    DirectObject = 2  # Yellow
    IndirectObject = 3  # Orange
    PredicateNominative = 4  # Pink
    PredicateAdjective = 5  # Purple
    PrepositionalPhrase = 6
    Appositive = 7
    Participle = 8
    Infinitive = 9


POS_MAP = {
    'N': POS.Noun.value,
    'V': POS.Verb.value,
    'DO': POS.DirectObject.value,
    'IO': POS.IndirectObject.value,
    'PN': POS.PredicateNominative.value,
    'PA': POS.PredicateAdjective.value,
    'APPOS': POS.Appositive.value,
    'PARTICIPLE': POS.Participle.value,
    'INF': POS.Infinitive.value
}