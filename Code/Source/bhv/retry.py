
from bhv import Node

class Retry(Node):
    def __init__(self, child: Node):
        self.child = child

    def start(self) -> None:
        self.child.start()

    def update(self, dt: float) -> Node.State:
        state = self.child.update(dt)
        if state == Node.State.FAILURE:
            self.child.start()
            return Node.State.RUNNING
        else:
            return state