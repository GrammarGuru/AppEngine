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
    'N': POS.Noun,
    'V': POS.Verb,
    'DO': POS.DirectObject,
    'IO': POS.IndirectObject,
    'PN': POS.PredicateNominative,
    'PA': POS.PredicateAdjective,
    'APPOS': POS.Appositive,
    'PARTICIPLE': POS.Participle,
    'INF': POS.Infinitive
}