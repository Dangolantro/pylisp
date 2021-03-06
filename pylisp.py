from EvalException import EvalException
from Token import Token
from Lexer import Lexer
from TokenType import TokenType
from globals import logOn
import traceback

env = {
    '+': lambda x,y: x[1]+y[1],
    '-': lambda x,y: x[1]-y[1],
    '*': lambda x,y: x[1]*y[1],
    '/': lambda x,y: x[1]/y[1]
}


def parse(program):
    return read_from_tokens(tokenize(program))


def tokenize(s):
    tokens = Lexer.tokenize(s)
    if logOn: print(f'LOG: {tokens}')
    return tokens


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
    elif token[0] == TokenType.APSTR:
        if len(tokens) == 0 or tokens[0][0] != TokenType.L_PAR:
            return token
        tokens.pop(0)
        ast = []
        while tokens[0][0] != TokenType.R_PAR:
            ast.append(read_from_tokens(tokens))
        tokens.pop(0)
        return [token, ast]
    elif token[0] == TokenType.PRIM or token[0] == TokenType.NUM:
        return atom(token)
    elif token[0] == TokenType.MATH_OP or token[0] == TokenType.ID or token[0] == TokenType.BOOL:
        return token
    else:
        raise SyntaxError('unexpected ' + token[1])


def atom(token):
    if token[0] == TokenType.PRIM:
        return token
    assert token[0] == TokenType.NUM
    try:
        return token[0], int(token[1])
    except ValueError:
        try:
            return token[0], float(token[1])
        except ValueError:
            return token


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
        ast = parse(input(prompt))
        if logOn: print(f'LOG: {ast}')
        try:
            out = format_string(Token.eval(ast, env))
            if out is not None:
                print(out)
        except EvalException as e:
            print(e.message)
            print('Environment: ')
            print(e.env)
            #print(traceback.format_exc())


# WIP
def format_string(out):
    type, val = out if isinstance(out, tuple) else out[0]
    if type == TokenType.NUM:
        return str(val)
    elif type == TokenType.BOOL:
        return val
    elif type == TokenType.APSTR:
        return f"({', '.join([format_string(el) for el in out[1]])})"

    return None


def main():
    repl()


if __name__ == '__main__':
    main()
