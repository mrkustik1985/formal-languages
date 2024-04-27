from copy import deepcopy as copy
from utils import Rule
from checker import check


SMB_START = '#'
SYMBL_END = '$'


class LR:
    def __init__(self):
        self.gram = None
        self.nds = None
        self.nds_st = None
        self.table = None

    class Configuration:
        def __init__(self, rule, next_smb, pnt_pos):
            self.rule = rule
            self.next_smb = next_smb
            self.pnt_pos = pnt_pos

        def __eq__(self, other):
            if isinstance(other, type(self)):
                return ((self.rule == other.rule) and
                        (self.next_smb == other.next_smb) and
                        (self.pnt_pos == other.pnt_pos))
            return False

        def __hash__(self):
            return hash((self.rule, self.next_smb, self.pnt_pos))

    class Node:
        def __init__(self):
            self.children = {}
            self.confs = set()

        def __eq__(self, other):
            if isinstance(other, type(self)):
                return self.confs == other.confs
            return False

        def __hash__(self):
            return hash(tuple(self.confs))

    class Shift:
        def __init__(self, to):
            self.to = to

    class Reduce:
        def __init__(self, rule):
            self.rule = rule

    def fit(self, gram):
        self.gram = gram
        self.nds = [self.Node()]
        self.nds[0].confs.add(self.Configuration(Rule(SMB_START, gram.start),
                                                 SYMBL_END, 0))
        self.nds[0] = self.closure(self.nds[0])
        self.nds_st = {self.nds[0]}
        i = 0
        while i < len(self.nds):
            processed = set()
            for conf in self.nds[i].confs:
                if ((len(conf.rule.right) > conf.pnt_pos) and
                        (conf.rule.right[conf.pnt_pos] not in processed)):
                    self.goto(i, conf.rule.right[conf.pnt_pos])
                    processed.add(conf.rule.right[conf.pnt_pos])
            i += 1
        self.table = [{} for _ in range(len(self.nds))]
        self.fill_table(0, set())

    def predict(self, word):
        word += SYMBL_END
        stack = [0]
        i = 0
        while i < len(word):
            alpha = word[i]
            stack_back = stack[-1]
            if alpha not in self.table[stack_back]:
                return False
            if isinstance(self.table[stack_back][alpha], self.Reduce):
                if self.table[stack_back][alpha].rule == Rule(
                        SMB_START, self.gram.start):
                    if i == (len(word) - 1):
                        return True
                    return False
                if (len(self.table[stack_back]
                        [alpha].rule.right) * 2) >= len(stack):
                    return False
                next_stack_elem = self.table[stack_back][alpha].rule.left
                rule_len = len(self.table[stack_back][alpha].rule.right)
                stack = stack[:len(stack) - (rule_len * 2)]
                stack_back = stack[-1]
                stack.append(next_stack_elem)
                stack.append(self.table[stack_back][next_stack_elem].to)

            elif isinstance(self.table[stack_back][alpha], self.Shift):
                stack.append(alpha)
                stack.append(self.table[stack_back][alpha].to)
                i += 1
        return False

    def closure(self, node):
        chng = True
        while chng:
            new_node = copy(node)
            chng = False
            for conf in node.confs:
                for rule in self.gram.rules():
                    if ((len(conf.rule.right) > conf.pnt_pos) and
                            (conf.rule.right[conf.pnt_pos] == rule.left)):
                        for next_smb in self.first(
                                conf.rule.right[conf.pnt_pos + 1:] +
                                conf.next_smb, set()):
                            if self.Configuration(
                                    rule, next_smb, 0) not in new_node.confs:
                                new_node.confs.add(
                                    self.Configuration(rule, next_smb, 0))
                                chng = True
            node = new_node

        return node

    def goto(self, i, chr):
        new_node = self.Node()
        for conf in self.nds[i].confs:
            if ((len(conf.rule.right) > conf.pnt_pos) and
                    (conf.rule.right[conf.pnt_pos] == chr)):
                new_node.confs.add(self.Configuration(conf.rule,
                                                      conf.next_smb,
                                                      conf.pnt_pos + 1))
        new_node = self.closure(new_node)
        if new_node not in self.nds_st:
            self.nds.append(new_node)
            self.nds_st.add(new_node)
        if chr in self.nds[i].children:
            raise Exception('Not LR(1) gram')
        self.nds[i].children[chr] = self.nds.index(new_node)

    def fill_table(self, i, used):
        if i in used:
            return

        for symbol in self.nds[i].children:
            self.table[i][symbol] = self.Shift(self.nds[i].children[symbol])

        for conf in self.nds[i].confs:
            if len(conf.rule.right) == conf.pnt_pos:
                if conf.next_smb in self.table[i]:
                    raise Exception('Not LR(1) gram')
                self.table[i][conf.next_smb] = self.Reduce(conf.rule)
        used.add(i)
        for symbol in self.nds[i].children:
            self.fill_table(self.nds[i].children[symbol], used)

    def first(self, w, cur_oppend):
        if w in cur_oppend:
            return set()
        cur_oppend.add(w)
        if len(w) == 0:
            return set()
        res = [w[0]]
        res_set = {w[0]}
        if self.gram.is_terminal(w):
            return res_set
        chng = True
        while chng:
            chng = False
            u_index = 0
            while u_index < len(res):
                alpha = res[u_index]
                if self.gram.is_terminal(alpha):
                    break
                chng = chng or self.add_not_term_first(alpha, res, res_set)
                u_index += 1

        if '' in res_set:
            res_set.remove('')
            res_set.update(self.first(w[1:], cur_oppend))
        return res_set

    def add_not_term_first(self, alpha, res, res_set):
        chng = False
        for rule in self.gram.rules():
            if rule.left != alpha:
                continue
            if alpha in res_set:
                chng = True
                res_set.discard(alpha)
            if ((alpha != rule.right[:1]) and
                    (rule.right[:1] not in res_set)):
                chng = True
                res_set.add(rule.right[:1])
                res.append(rule.right[:1])
        return chng


if __name__ == '__main__':
    check(LR())
