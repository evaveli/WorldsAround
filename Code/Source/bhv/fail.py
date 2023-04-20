
from bhv import Node

class Fail(Node):
    def __init__(self, child: Node):
        self.child = child

    def start(self) -> None:
        self.child.start()

    def update(self, dt: float) -> Node.State:
        state = self.child.update(dt)
        if state == Node.State.SUCCESS:
            return Node.State.FAILURE
        else:
            return state