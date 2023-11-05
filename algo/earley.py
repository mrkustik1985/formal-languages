from state import rule, situation
class earley_parser:
  def __init__(self):
    self.G = {}
    self.not_term = {}

  def fit(self, G):
    self.G = G
    for rule in G:
      self.not_term[rule.left] = rule.right

  def scan(self, D, j, w):
    if j == 0:
      return 0
    for sit in D[j - 1]:
      if len(sit.rule.right) > sit.pos_rule and sit.rule.right[sit.pos_rule] == w[j - 1]:
        D[j].add(situation(sit.rule, sit.cnt_let + 1, sit.pos_rule + 1, sit.cnt_let_before))
  
  def complete(self, D, j):
    D_nw = set()
    for sti_up in D[j]:
      if sti_up.pos_rule >= len(sti_up.rule.right):
        for sti_f in D[sti_up.cnt_let_before]:
          try:
            if sti_up.rule.left == sti_f.rule.right[sti_f.pos_rule]:
              nd_ad = situation(sti_f.rule, j, sti_f.pos_rule + 1, sti_f.cnt_let_before)
              if nd_ad not in D[j]:
                D_nw.add(nd_ad)
          except Exception:
            pass
    D[j] = D[j] | D_nw
    return len(D_nw) != 0

  def predict(self, D, j):
    D_nw = set()
    for sit in D[j]:
      try:
        if sit.rule.right[sit.pos_rule] in self.not_term:
          for sit_dn in self.G:
            if sit_dn.left == sit.rule.right[sit.pos_rule]:
              nd_ad = situation(sit_dn, j, 0, j)
              if nd_ad not in D[j]:
                D_nw.add(situation(sit_dn, j, 0, j))
      except Exception:
        pass
    D[j] = D[j] | D_nw
    return len(D_nw) != 0

  def earley(self, w):
    D = [set() for i in range(len(w) + 1)]
    D[0].add(situation(rule('P', 'S'), 0, 0, 0))
    for i in range(len(w) + 1):
      self.scan(D, i, w)
      fl = True
      while fl:
        fl = False
        f1 = self.complete(D, i)
        f2 = self.predict(D, i)
        fl = (f1 | f2)
    if situation(rule('P', 'S'), len(w), 1, 0) in D[len(w)]:
      return True
    return False

def fit(tree_obj, G):
  tree_obj.fit(G)

def predict(tree_obj, w):
  return tree_obj.earley(w)  

if __name__ == '__main__':
  n = int(input())
  G = set()
  G.add(rule('P', 'S'))
  for i in range(n):
    rl = input().split('->')
    G.add(rule(rl[0], rl[1]))
  tree_obj = earley_parser()
  fit(tree_obj, G)

  w = input()

  print(predict(tree_obj, w))
  
'''
3
S->aSa
S->
S->bS
abbba

YES
'''
'''
4
S->abaS
S->A
A->cdA
A->dd
abaccdd

NO
'''