from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from .search import BasicSearch

class BreadthFirstSearch(BasicSearch):
    @staticmethod 
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
        
        Returns:
            Solution: Solution found
        """
        # Create a node for the start cell
        start = grid.get_node(pos=grid.start)
        frontier = QueueFrontier()
        frontier.add(start)

        # keep track of explored positions
        explored_states = set() 

        while not frontier.is_empty():
            # Remove node from the frontier
            node = frontier.remove()

            # Add current node position to explored set
            explored_states.add(node.state)

            # Check if this is the destination point
            if node.state == grid.end:
                # Generate path and return a Solution object
                path, path_cost = BreadthFirstSearch.generate_path(node, grid)
                return Solution(path=path, 
                                explored_states=list(explored_states), 
                                path_cost=path_cost
                                )
            
            # Explore neighbors
            neighbors = grid.get_neighbors(node.state)
            for action, state in neighbors.items():
                if state in explored_states or frontier.contains_state(state):
                    continue 

                new = grid.get_node(pos=state) 
                new.parent = node
                new.action = action 

                frontier.add(node=new)
        
        return NoSolution([], list(explored_states))