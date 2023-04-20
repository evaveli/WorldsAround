
from bhv import Node

class Loop(Node):
    def __init__(self, child: Node):
        self.child = child

    def start(self) -> None:
        self.child.start()

    def update(self, dt: float) -> Node.State:
        self.child.update(dt)
        return Node.State.RUNNING