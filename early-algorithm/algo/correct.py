from state import rule, situation

not_term = {}

def scan(D, G, j, w):
  if j == 0:
    return 0
  for sit in D[j - 1]:
    if len(sit.rule.right) > sit.pos_rule and sit.rule.right[sit.pos_rule] == w[j - 1]:
      # print(len(sit.rule.right), " WTF", j, sit.rule.left, sit.rule.right, sit.pos_rule + 1, sit.cnt_let + 1)
      D[j].add(situation(sit.rule, sit.cnt_let + 1, sit.pos_rule + 1, sit.cnt_let_before))

def complete(D, j, G, w):
  D_nw = set()
  for sti_up in D[j]:
    if sti_up.pos_rule >= len(sti_up.rule.right):
      for sti_f in D[sti_up.cnt_let_before]:
        try:
          if sti_up.rule.left == sti_f.rule.right[sti_f.pos_rule]:
            nd_ad = situation(sti_f.rule, j, sti_f.pos_rule + 1, sti_f.cnt_let_before)
            if nd_ad not in D[j]:
              # print("AD complete ", sti_f.rule.left, sti_f.rule.right, j, sti_f.pos_rule + 1)
              D_nw.add(nd_ad)
        except Exception:
          pass
  D[j] = D[j] | D_nw
  return len(D_nw) != 0

def predict(D, j, G, w):
  D_nw = set()
  for sit in D[j]:
    try:
      if sit.rule.right[sit.pos_rule] in not_term:
        for sit_dn in G:
          if sit_dn.left == sit.rule.right[sit.pos_rule]:
            nd_ad = situation(sit_dn, j, 0, j)
            if nd_ad not in D[j]:
              # print("ad predict", sit_dn.left, sit_dn.right, sit.cnt_let, sit.pos_rule)
              D_nw.add(situation(sit_dn, j, 0, j))
    except Exception:
      pass
  D[j] = D[j] | D_nw
  return len(D_nw) != 0

def earley(G, w):
  D = [set() for i in range(len(w) + 1)]
  D[0].add(situation(rule('P', 'S'), 0, 0, 0))
  for i in range(len(w) + 1):
    scan(D, G, i, w)
    fl = True
    while fl:
      fl = False
      f1 = complete(D, i, G, w)
      f2 = predict(D, i, G, w)
      fl = (f1 | f2)
    # print("start print D ", i)
    # for x in D[i]:
    #   print(x.rule.left, x.rule.right, x.cnt_let, x.pos_rule, x.cnt_let_before)
  if situation(rule('P', 'S'), len(w), 1, 0) in D[len(w)]:
    return True
  return False

if __name__ == '__main__':
  n = int(input())
  G = set()
  not_term['P'] = 'S'
  G.add(rule('P', 'S'))
  for i in range(n):
    rl = input().split('->')
    not_term[rl[0]] = rl[1]
    G.add(rule(rl[0], rl[1]))
  w = input()
  print(earley(G, w))

'''
3
S->aSa
S->
S->bS
abba

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