class TokenType:
    L_PAR = 0
    R_PAR = 1
    MATH_OP = 2
    PRIM = 3
    NUM = 4
    ID = 5
    APSTR = 6
    BOOL = 7

    math_ops = {'+', '-', '*', '/'}
    prims = {'eq?', 'quote', 'cons', 'car', 'cdr', 'atom?', 'define', 'lambda', 'cond'}
    arg_count = {
        'eq?': 2,
        'define': 2,
        'quote': 1,
        'car': 1,
        'cdr': 1,
        'lambda': 2,
        'cons': 2
    }