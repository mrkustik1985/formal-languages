import pytest
from utils import Rule
from lr import LR


@pytest.mark.parametrize('nonterms', [{*'S'}])
@pytest.mark.parametrize('terms', [{*'()'}])
@pytest.mark.parametrize('rules', [{Rule('S', '(S)S'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_bracket_sequences_same(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('')
    assert not algo.predict('(')
    assert not algo.predict(')')
    assert algo.predict('()')
    assert algo.predict('()()')
    assert algo.predict('(())')
    assert not algo.predict('(()')
    assert not algo.predict(')()')
    assert not algo.predict(')()(')


@pytest.mark.parametrize('nonterms', [{*'S'}])
@pytest.mark.parametrize('terms', [{*'()[]{}'}])
@pytest.mark.parametrize('rules', [{Rule('S', '(S)S'),
                         Rule('S', '[S]S'), Rule('S', '{S}S'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_bracket_sequences_mixed(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('')
    assert algo.predict('()')
    assert algo.predict('[]{}')
    assert not algo.predict('[(])')
    assert not algo.predict('[{)]')
    assert algo.predict('([]){}')


@pytest.mark.parametrize('nonterms', [{*'S'}])
@pytest.mark.parametrize('terms', [{*'a'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'aS'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_a_star(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('')
    assert algo.predict('a')
    assert algo.predict('aa')
    assert not algo.predict('ab')


@pytest.mark.parametrize('nonterms', [{*'SB'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules',
                         [{Rule('S', 'aB'), Rule('B', 'b'), Rule('B', 'ba')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_aB(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('ab')
    assert algo.predict('aba')
    assert not algo.predict('a')
    assert not algo.predict('ba')
    assert not algo.predict('abab')
    assert not algo.predict('abaa')
    assert not algo.predict('ab ')
    assert not algo.predict('aba ')


@pytest.mark.parametrize('nonterms', [{*'S'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'aSbS'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_aSbS(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('aababb')
    assert not algo.predict('aabbba')
    assert algo.predict('ab')
    assert not algo.predict('abb')
    assert not algo.predict('abbbbb')
    assert not algo.predict('ba')
    assert not algo.predict('b')
    assert not algo.predict('a')
    assert not algo.predict('baa')
    assert not algo.predict('aba')
    assert algo.predict('abab')
    assert algo.predict('ababababab')
    assert algo.predict('aaabbbababab')
    assert algo.predict('')
    assert not algo.predict(' ')


@pytest.mark.parametrize('nonterms', [{*'SFG'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize(
    'rules', [
        {
            Rule(
                'S', 'aFbF'), Rule(
                    'F', 'aFb'), Rule(
                        'F', ''), Rule(
                            'F', 'Ga'), Rule(
                                'G', 'bSG')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_aFb_with_G(grammar):
    algo = LR()
    with pytest.raises(Exception):
        algo.fit(grammar)


@pytest.mark.parametrize('nonterms', [{*'SFG'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules',
                         [{Rule('S', 'aFbF'),
                           Rule('F', 'aFb'),
                           Rule('F', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_aFb(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('aabb')
    assert algo.predict('abab')
    assert not algo.predict('ababab')
    assert algo.predict('aabbab')
    assert algo.predict('aabbaaabbb')
    assert not algo.predict('a')
    assert not algo.predict('aa')
    assert not algo.predict('aabbb')
    assert not algo.predict('aabb ')
    assert not algo.predict('ba')
    assert not algo.predict('baa')


@pytest.mark.parametrize('nonterms', [{*'SA'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules',
                         [{Rule('A', 'S'), Rule('S', 'aSbS'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'A')
def test_algo_AS(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('aababb')
    assert not algo.predict('aabbba')
    assert algo.predict('ab')
    assert not algo.predict('abb')
    assert not algo.predict('abbbbb')
    assert not algo.predict('ba')
    assert not algo.predict('b')
    assert not algo.predict('a')
    assert not algo.predict('baa')
    assert not algo.predict('aba')
    assert algo.predict('abab')
    assert algo.predict('ababababab')
    assert algo.predict('aaabbbababab')
    assert algo.predict('')
    assert not algo.predict(' ')


@pytest.mark.parametrize('nonterms', [{*'SA'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules', [{Rule('A', 'S'),
                         Rule('S', 'aSbS'), Rule('S', 'bSaS'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'A')
def test_algo_aSbS_and_bSaS(grammar):
    algo = LR()
    with pytest.raises(Exception):
        algo.fit(grammar)


@pytest.mark.parametrize('nonterms', [{*'SA'}])
@pytest.mark.parametrize('terms', [{*'ab'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'SaSb'), Rule('S', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_SaSb(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('aabbab')
    assert algo.predict('ab')
    assert algo.predict('ababababab')
    assert not algo.predict('ababababba')
    assert not algo.predict('abb')
    assert not algo.predict('abbbbb')
    assert not algo.predict('ba')
    assert not algo.predict('b')
    assert not algo.predict('a')
    assert not algo.predict('baa')
    assert not algo.predict('aba')
    assert algo.predict('abab')
    assert algo.predict('ababababab')
    assert algo.predict('aaabbbababab')
    assert algo.predict('')
    assert not algo.predict(' ')
    assert not algo.predict('abba')
    assert not algo.predict('babababa')
    assert not algo.predict('bababab')


@pytest.mark.parametrize('nonterms', [{*'SBC'}])
@pytest.mark.parametrize('terms', [{*'abc'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'Bb'),
                         Rule('B', 'a'), Rule('S', 'Cc'), Rule('C', 'a')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_ABC(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('ab')
    assert algo.predict('ac')
    assert not algo.predict('a')
    assert not algo.predict('abc')
    assert not algo.predict('abb')
    assert not algo.predict('abbbbb')
    assert not algo.predict('ba')
    assert not algo.predict('b')
    assert not algo.predict('a')
    assert not algo.predict('baa')
    assert not algo.predict('aba')
    assert not algo.predict('abab')
    assert not algo.predict('ababababab')
    assert not algo.predict('aaabbbababab')
    assert not algo.predict('')
    assert not algo.predict(' ')
    assert not algo.predict('abba')
    assert not algo.predict('babababa')
    assert not algo.predict('bababab')


@pytest.mark.parametrize('nonterms', [{*'SBC'}])
@pytest.mark.parametrize('terms', [{*'abc'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'B'),
                         Rule('B', 'baa'), Rule('S', ''), Rule('B', 'baaa')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_SBC(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('baa')
    assert algo.predict('baaa')
    assert not algo.predict('ba')
    assert not algo.predict('baaaa')
    assert not algo.predict('abb')
    assert not algo.predict('abbbbb')
    assert not algo.predict('ba')
    assert not algo.predict('b')
    assert not algo.predict('a')
    assert not algo.predict('aba')
    assert not algo.predict('abab')
    assert not algo.predict('ababababab')
    assert not algo.predict('aaabbbababab')
    assert algo.predict('')
    assert not algo.predict(' ')
    assert not algo.predict('abba')
    assert not algo.predict('babababa')
    assert not algo.predict('bababab')


@pytest.mark.parametrize('nonterms', [{*'SBC'}])
@pytest.mark.parametrize('terms', [{*'abc'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'B'),
                         Rule('B', 'baa'), Rule('S', 'C'), Rule('C', 'baa')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_BC(grammar):
    algo = LR()
    with pytest.raises(Exception):
        algo.fit(grammar)


@pytest.mark.parametrize('nonterms', [{*'SAB'}])
@pytest.mark.parametrize('terms', [{*'abc'}])
@pytest.mark.parametrize('rules',
                         [{Rule('S',
                                'SABSBASABAABSSSAAABBBSSSBBBAAAabc'),
                           Rule('S',
                                ''),
                             Rule('A',
                                  ''),
                             Rule('B',
                                  '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_SABS(grammar):
    algo = LR()
    with pytest.raises(Exception):
        algo.fit(grammar)


@pytest.mark.parametrize('nonterms', [{*'SAB'}])
@pytest.mark.parametrize('terms', [{*'abc'}])
@pytest.mark.parametrize('rules', [{Rule('S', 'SABBAabc'),
                         Rule('S', ''), Rule('A', ''), Rule('B', '')}])
@pytest.mark.parametrize('start', 'S')
def test_algo_SAB(grammar):
    algo = LR()
    algo.fit(grammar)
    assert algo.predict('abc')
    assert not algo.predict('a')
    assert not algo.predict('b')
    assert not algo.predict('c')
    assert not algo.predict('bc')
    assert not algo.predict('ab')
    assert not algo.predict('ac')
    assert algo.predict('abcabc')
    assert algo.predict('abcabcabc')
    assert not algo.predict('abcab')
    assert algo.predict('')
