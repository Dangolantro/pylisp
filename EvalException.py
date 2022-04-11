class EvalException(Exception):

    def __init__(self, env, msg):
        self.env = env
        self.message = msg
        super().__init__(self.message)
