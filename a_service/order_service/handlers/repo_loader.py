
from repository import OrderRep

class Handler:
    def __init__(self, repo: OrderRep):
        self.repo = repo

    def execute(self):
        pass

class OrderCode(Handler):
    def execute(self, order_code):
        return self.repo.load_for_order_code(order_code)
    
class RepoLoader:
    @staticmethod
    def factory(cmd, data, repo):
        cmds = {
            "order_code": OrderCode,
        }
        if cmd in cmds:
            return cmds[cmd](repo).execute(data)
        else:
            raise ValueError(f"Unknown command: {cmd}")