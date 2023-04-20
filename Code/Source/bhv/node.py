
import abc
import enum


class Node(metaclass=abc.ABCMeta):
    """
        A node is a single unit of behavior.

        Methods
        -------
        start(): None
            (Optional) Called when the node is first started.
        update(dt: float) -> Node.State
            Update the state of the node.
            Called every frame until it returns `State.SUCCESS` or `State.Failure`.
    """

    class State(enum.Enum):
        """ The state of a node. """

        SUCCESS = 0
        FAILURE = 1
        RUNNING = 2

    def start(self) -> None:
        """ (Optional) Called when the node is first started. """

        pass

    @abc.abstractmethod
    def update(self, dt: float) -> State:
        """
            Update the state of the node and returns its current state.
            This function is called every frame.

            Parameters
            ----------
            dt : float
                The time passed since the last frame.
        """
        pass