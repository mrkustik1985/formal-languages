class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        if isinstance(other, Rule):
            return (self.left == other.left) and (self.right == other.right)
        return False

    def __hash__(self):
        return hash((self.left, self.right))


class Grammar:
    def __init__(self, nonterms, terms):
        self.nonterms = nonterms
        self.terms = terms
        self._rules = set()

    def add_rule(self, rule):
        self._rules.add(rule)

    def is_terminal(self, let):
        return let in self.terms

    def rules(self):
        return self._rules
