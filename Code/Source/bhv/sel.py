
from bhv import Node


class Selector(Node):
    def __init__(self, children: list[Node]) -> None:
        self.children = children
        self.current = 0

    def start(self) -> None:
        self.current = 0
        self.children[self.current].start()

    def update(self, dt: float) -> Node.State:
        while True:
            if self.current >= len(self.children):
                self.current = 0
                return Node.State.FAILURE

            state = self.children[self.current].update(dt)
            if state == Node.State.FAILURE:
                self.current += 1
            else:
                return state