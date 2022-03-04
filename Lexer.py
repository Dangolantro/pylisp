from Token import Token

class Lexer:
    @staticmethod
    def tokenize(prg: str) -> list:
        items = prg.replace('(', ' ( ') \
                .replace(')', ' ) ') \
                .split()

        result = []
        for i in items:
            result.append(Token.get_token(i))

        return result