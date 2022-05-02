from copy import copy
from TokenType import TokenType
from EvalException import EvalException


class Token:
    @staticmethod
    def get_token(s: str) -> tuple[int, str]:
        tkn_type = -1

        if s == '(':
            tkn_type = TokenType.L_PAR
        elif s == ')':
            tkn_type = TokenType.R_PAR
        elif s[0] == "'":
            tkn_type = TokenType.APSTR
        elif s == "#f" or s == "#t":
            tkn_type = TokenType.BOOL
        elif s.replace('.', '', 1).isdigit():
            tkn_type = TokenType.NUM
        elif s in TokenType.math_ops:
            tkn_type = TokenType.MATH_OP
        elif s in TokenType.prims:
            tkn_type = TokenType.PRIM
        else:
            tkn_type = TokenType.ID

        return tkn_type, s

    @staticmethod
    def make_bool(b):
        return (TokenType.BOOL, '#t' if b else '#f')

    @staticmethod
    def eval(expr, env: dict):
        try:
            tkn_type, val = expr[0] if isinstance(expr, list) else expr
            if tkn_type == TokenType.NUM:
                return (tkn_type, val)
            elif tkn_type == TokenType.ID:
                if val not in env:
                    raise Exception(f"Reference to undefined object '{val}'")
                obj = env[val]
                if 'args' in obj:
                    if len(expr)-1 != len(obj['args']):
                        raise Exception(f"{val} operation expected {len(obj['args'])} arguments")
                    fn_env = copy(env)
                    for aName,arg in zip(obj['args'],expr[1:]):                      
                        fn_env[aName[1]] = Token.eval(arg, env)
                    return Token.eval(obj['expr'], fn_env)
                return obj
            elif tkn_type == TokenType.MATH_OP:
                return (TokenType.NUM, env[val](Token.eval(expr[1], env), Token.eval(expr[2], env)))
            elif tkn_type == TokenType.PRIM:
                # Verify expression contains correct number of arguments
                if val != 'cond':
                    arg_count = TokenType.arg_count[val]
                    if len(expr)-1 != arg_count:
                        raise Exception(f"Wrong number of arguments for '{val}', expected {arg_count}")

                if val == 'define':
                    # TODO: make sure ID name is valid,
                    env[expr[1][1]] = Token.eval(expr[2], env)
                elif val == 'eq?':
                    return Token.make_bool(
                        Token.eval(expr[1], env) == Token.eval(expr[2], env))
                elif val == 'quote':
                    if isinstance(expr[1], list):
                        return [(6, "'"), expr[1]]
                    return expr[1][1]
                elif val == 'car' or val == 'cdr':
                    lst = Token.eval(expr[1], env)
                    if not isinstance(lst, list) or len(lst) != 2:
                        raise Exception(f"{val} operation expected a list as parameter")
                    if len(lst[1]) == 0:
                        raise Exception(f"{val} operation cannot proceed on list of length 0")
                    if val == 'car':
                        return lst[1][0]
                    # cdr
                    tmp = copy(lst[1])
                    tmp.pop(0)
                    return [(TokenType.APSTR, "'"), tmp]
                elif val == 'lambda':
                    if any(tok[0] != TokenType.ID for tok in expr[1]):
                        raise Exception(f"lamba args expected to be valid identifiers")
                    return {
                        'args': expr[1],
                        'expr': expr[2]
                    }
                elif val == 'cons':
                    return [(6, "'"), [Token.eval(expr[1], env), Token.eval(expr[2], env)]]
                elif val == 'cond':
                    for t in expr[1:]:
                        e0 = Token.eval(t[0], env)
                        if e0[0] != TokenType.BOOL:
                            raise Exception(f"one or more cond tests are not bools")
                        if e0[1] == "#t":
                            return Token.eval(t[1], env)

            elif tkn_type == TokenType.APSTR:
                if isinstance(expr, list) and len(expr) > 1:
                    return expr
                return expr[1][1:]
            return expr
        except Exception as e:
            raise EvalException(env, str(e)) from e
