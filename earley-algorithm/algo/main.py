from state import rule, situation
from earley import  earley_parser
from earley import  fit, predict

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
