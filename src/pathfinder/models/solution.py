class Solution:
    """Model a solution to a pathfinding problem"""

    def __init__(
            self, 
            path: list[tuple[int, int]],
            explored_states: list[tuple[int, int]],
            time: float = 0.0,
            path_cost: int = 0
    ) -> None:
        self.path = path
        self.path_cost = path_cost
        self.path_length = len(path)
        self.explored_states = explored_states
        self.explored_length = len(explored_states)
        self.time = time

    def __repr__(self) -> str:
        return f"Solution([{self.path[0]}, ..., {self.path[-1]}], {self.path_cost}, {self.time})"

class NoSolution(Solution):
    """Model an empty pathfinding solution"""

    def __repr__(self) -> str:
        explored_states = list(self.explored_states)
        return f"NoSolution([], [{explored_states[0]}, ..., {explored_states[-1]}], {self.time})"
    