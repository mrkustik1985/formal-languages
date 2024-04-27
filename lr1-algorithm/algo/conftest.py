import pytest

from utils import Grammar


@pytest.fixture
def grammar(nonterms, terms, rules, start):
    result = Grammar(nonterms, terms)
    for rule in rules:
        result.add_rule(rule)
    result.start = start
    return result
