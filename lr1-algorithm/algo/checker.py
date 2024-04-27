from utils import Rule, Grammar


def check(algorithm):
    nonterm_count, term_count, rules_count = map(int, input().split())
    nonterms = {x for x in input()}
    terms = {x for x in input()}
    grammar = Grammar(nonterms, terms)
    for i in range(rules_count):
        row = input()
        for letter in row:
            if ((letter not in set(['-', '>'])) and
                    (letter not in nonterms) and
                    (letter not in terms)):
                raise Exception('Wrong input format')
        grammar.add_rule(Rule(*row.split('->')))
    try:
        grammar.start = input()
    except BaseException:
        raise Exception('Wrong input format')

    if grammar.start not in nonterms:
        raise Exception('Start symbol is not a nonterminal')

    if not grammar.is_context_free():
        raise Exception('Wrong grammar')

    algorithm.fit(grammar)

    words_count = int(input())
    for i in range(words_count):
        word = input()
        for letter in word:
            if not grammar.is_terminal(letter):
                raise Exception('Wrong word')
        print('Yes' if algorithm.predict(word) else 'No')
