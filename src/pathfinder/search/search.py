from ..models.grid import Grid
from ..models.node import Node


class BasicSearch: 
    @staticmethod
    def generate_path(node: Node, grid: Grid) -> tuple[list[tuple[int, int]], int]:
        # Generate path from start to goal
        path = []
        path_cost = 0

        curr = node
        while curr.parent:
            path.append(curr.state)
            path_cost += curr.cost 
            curr = curr.parent
        
        path.append(grid.start)
        path.reverse()
        return path, path_cost