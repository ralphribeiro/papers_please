from dataclasses import dataclass, field
from functools import partial
from itertools import chain
import re
from typing import Iterable


def parse_string(str):
    """Parse  """

@dataclass()
class Bulletin:
    regulations: str


def find_patterns(target: str, pattern1: Iterable, pattern2: Iterable) -> dict:
    ret = {}
    for t in target.split('\n'):
        p = re.compile('|'.join(pat for pat in pattern1))
        finded = p.search(t)
        if finded:
            p2 = re.compile('|'.join(pat for pat in pattern2))
            finded2 = p2.finditer(t)
            if finded2:
                ret[finded.group()] = tuple(r.group() for r in finded2)
    return ret


def nations_regulation(countries: Iterable, regulation: str) -> dict:
    """ Structuring nations regulations.

    Args:
        regulation (str): raw regulation
        countries (Iterable): iterable of countries

    Returns:
        dict: dictionary structured nations regulations
    """
    p1 = 'Allow', 'Deny'
    return find_patterns(regulation, p1, countries)


def documents_regulation(countries: Iterable, regulation: str) -> dict:
    """ Structuring documents regulations.

    Args:
        regulation (str): raw regulation
        countries (Iterable): iterable of countries

    Returns:
        dict: dictionary structured documents regulations
    """
    p1 = 'Foreigners', 'Citizens', 'Workers'
    p2_ = 'require', 'pass', 'access', 'permit', 'work', 'ID card'
    p2 = chain(countries, p2_)
    return find_patterns(regulation, p1, p2)


def vaccination_regulation(countries: Iterable, regulation: str) -> dict:
    """ Structuring documents regulations.

    Args:
        regulation (str): raw regulation
        countries (Iterable): iterable of countries

    Returns:
        dict: dictionary structured documents regulations
    """
    ...

regulations_funcs = (
    nations_regulation,
    documents_regulation
)


def regulations(regulation: str) -> dict:
    """ Structuring the regulations.

    Args:
        regulation (str): raw regulation

    Returns:
        dict: dictionary structured regulations
    """
    regulations = {}

    # Nations
    countries = (
        'Arstotzka', 'Antegria', 'Impor', 'Kolechia',
        'Obristan', 'Republia', 'United Federation'
    )

    # load nations
    fns = (partial(fn, countries) for fn in regulations_funcs)

    for fn in fns:
        regulations.update(fn(regulation))        

    return regulations
