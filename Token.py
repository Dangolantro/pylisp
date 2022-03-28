from TokenType import TokenType


class Token:
    @staticmethod
    def get_token(s: str) -> tuple[int, str]:
        tkn_type = -1

        if s == '(':
            tkn_type = TokenType.L_PAR
        elif s == ')':
            tkn_type = TokenType.R_PAR
        elif s == "'":
            tkn_type = TokenType.NO_EVAL
        elif s.replace('.', '', 1).isdigit():
            tkn_type = TokenType.NUM
        elif s in TokenType.math_ops:
            tkn_type = TokenType.MATH_OP
        elif s in TokenType.prims:
            tkn_type = TokenType.PRIM
        else:
            tkn_type = TokenType.ID

        return tkn_type, s
