from Lexer import Lexer
from TokenType import TokenType

Id = str
Primitive = str
BinOp = str
Number = (int, float)


def parse(program):
    return read_from_tokens(tokenize(program))


def tokenize(s):
    return Lexer.tokenize(s)


def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if token[0] == TokenType.L_PAR:
        ast = []
        while tokens[0][0] != TokenType.R_PAR:
            ast.append(read_from_tokens(tokens))
        tokens.pop(0)
        return ast
    elif token[0] == TokenType.PRIM or token[0] == TokenType.ID:
        return atom(token)
    elif token[0] == TokenType.MATH_OP:
        return BinOp(token[1])
    else:
        raise SyntaxError('unexpected ' + token[1])


def atom(token):
    if token[0] == TokenType.PRIM:
        return Primitive(token[1])
    assert token[0] == TokenType.ID
    try:
        return int(token[1])
    except ValueError:
        try:
            return float(token[1])
        except ValueError:
            return Id(token[1])


def standard_env():
    return Env()


class Env(dict):
    None


global_env = standard_env()


def repl(prompt='lisp> '):
    while True:
        # val = eval(parse(input(prompt)))
        # if val is not None:
        #     print(lispstr(val))
        # val = eval(parse(input(prompt)))
        # if val is not None:
        #     print(lispstr(val))
        val = parse(input(prompt))
        if val is not None:
            print(val)


def lispstr(exp):
    return ''


class Procedure():
    None


def eval(l, env=global_env):
    return ''


def main():
    repl()


if __name__ == '__main__':
    main()
