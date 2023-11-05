class rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash((self.left, self.right))


class situation:
    def __init__(self, rule : rule, cnt_let : int, pos_rule, cnt_let_bf : int):
        self.rule = rule
        self.cnt_let = cnt_let
        self.pos_rule = pos_rule
        self.cnt_let_before = cnt_let_bf

    def __eq__(self, other):
        return self.rule == other.rule and self.cnt_let == other.cnt_let and self.pos_rule == other.pos_rule and self.cnt_let_before == other.cnt_let_before
    
    def __hash__(self):
        return hash((self.rule, self.cnt_let, self.pos_rule, self.cnt_let_before))
