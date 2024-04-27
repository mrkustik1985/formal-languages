from state import rule, situation
from neterminal import base_neterminal1, base_neterminal2
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
    not_used_sit = {}
    for sti_up in D[j]:
      cnt = sti_up.cnt_let_before
      if cnt not in not_used_sit:
        not_used_sit[cnt] = set(D[cnt])
    for sti_up in D[j]:
      if sti_up.pos_rule >= len(sti_up.rule.right):
        cnt = sti_up.cnt_let_before
        dlt_sits = set()
        for sti_f in not_used_sit[cnt]:
          if len(sti_f.rule.right) == sti_f.pos_rule:
            continue
          if sti_up.rule.left == sti_f.rule.right[sti_f.pos_rule]:
            nd_ad = situation(sti_f.rule, j, sti_f.pos_rule + 1, sti_f.cnt_let_before)
            if nd_ad not in D[j]:
              D_nw.add(nd_ad)
              dlt_sits.add(sti_f)
        not_used_sit[cnt] -= dlt_sits
    D[j] = D[j] | D_nw
    return len(D_nw) != 0

  def predict(self, D, j):
    D_nw = set()
    rules_to_prdct = set(self.G)
    for sit in D[j]:
      if len(sit.rule.right) == sit.pos_rule:
        continue
      if sit.rule.right[sit.pos_rule] in self.not_term:
        dlt_rules = set()
        for sit_dn in rules_to_prdct:
          if sit_dn.left == sit.rule.right[sit.pos_rule]:
            nd_ad = situation(sit_dn, j, 0, j)
            if nd_ad not in D[j]:
              D_nw.add(situation(sit_dn, j, 0, j))
              dlt_rules.add(sit_dn)
        rules_to_prdct -= dlt_rules
    D[j] = D[j] | D_nw
    return len(D_nw) != 0

  def earley(self, w):
    D = [set() for i in range(len(w) + 1)]
    D[0].add(situation(rule(base_neterminal1, base_neterminal2), 0, 0, 0))
    for i in range(len(w) + 1):
      self.scan(D, i, w)
      fl = True
      while fl:
        fl = False
        f1 = self.complete(D, i)
        f2 = self.predict(D, i)
        fl = (f1 | f2)
    if situation(rule(base_neterminal1, base_neterminal2), len(w), 1, 0) in D[len(w)]:
      return True
    return False

def fit(tree_obj, G):
  tree_obj.fit(G)

def predict(tree_obj, w):
  if tree_obj.earley(w):
    return 'YES'
  return 'NO'