class TokenType():
    L_PAR = 0
    R_PAR = 1
    MATH_OP = 2
    PRIM = 3
    ID = 4

    math_ops = {'+', '-', '*', '/'}
    prims = {'eq?', 'quote', 'cons', 'car', 'cdr', 'atom?', 'define', 'lambda', 'cond'}