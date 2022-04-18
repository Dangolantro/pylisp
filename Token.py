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
    def eval(expr, env: dict):
        try:
            tkn_type, val = expr[0] if isinstance(expr, list) else expr
            if tkn_type == TokenType.NUM:
                return val
            elif tkn_type == TokenType.ID:
                if val not in env:
                    raise Exception(f"Reference to undefined object '{val}'")
                return env[val]
            elif tkn_type == TokenType.MATH_OP:
                return env[val](Token.eval(expr[1], env), Token.eval(expr[2], env))
            elif tkn_type == TokenType.PRIM:
                # Verify expression contains correct number of arguments
                arg_count = TokenType.arg_count[val]
                if len(expr)-1 != arg_count:
                    raise Exception(f"Wrong number of arguments for '{val}', expected {arg_count}")

                if val == 'define':
                    # TODO: make sure ID name is valid,
                    env[expr[1][1]] = Token.eval(expr[2], env)
                elif val == 'eq?':
                    return Token.eval(expr[1], env) == Token.eval(expr[2], env)
                elif val == 'quote':
                    if isinstance(expr[1], list):
                        return [(6, "'"), expr[1]]
                    return expr[1][1]
            elif tkn_type == TokenType.APSTR:
                if isinstance(expr, list) and len(expr) > 1:
                    return expr
                return expr[1][1:]
        except Exception as e:
            raise EvalException(env, str(e)) from e
