
from bhv import Node

class Nop(Node):
    def start(self) -> None:
        pass

    def update(self, dt: float) -> Node.State:
        return Node.State.SUCCESS