def parse(program):
    return read_from_tokens(tokenize(program))


def tokenize(s):
    None

def read_from_tokens(tokens):
    return None


def atom(token):
    None


def standard_env():
    return Env()


class Env(dict):
    None

global_env = standard_env()


def repl(prompt='lisp> '):
    while True:
        val = eval(parse(input(prompt)))
        if val is not None:
            print(lispstr(val))


def lispstr(exp):
    return ''


class Procedure():
    None


def eval(l, env=global_env):
    return ''
