from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from .search import BasicSearch

class GreedyBestFirstSearch(BasicSearch):
    @staticmethod 
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search Algorithm
        
        Args:
            grid (Grid): Grid of points
        
        Returns:
            Solution: Solution found
        """
        # Create node for the start cell
        start = grid.get_node(pos=grid.start)

        # Instantiate PriorityQueue frontier and add start node into it
        frontier = PriorityQueueFrontier()
        frontier.add(
            node=start, 
            priority=GreedyBestFirstSearch.heuristic(grid.start, grid.end)
        )

        # Keep track of explored positions
        explored_states = set()

        while not frontier.is_empty():
            # Remove node from the frontier
            node = frontier.remove()
            # Add current node position to explored set
            explored_states.add(node.state)

            # Check if this is the destination point
            if node.state == grid.end:
                path, path_cost = GreedyBestFirstSearch.generate_path(node, grid)
                return Solution(path=path,
                                explored_states=list(explored_states),
                                path_cost=path_cost
                                )
            
            # Explore neighbors
            neighbors = grid.get_neighbors(node.state)
            for action, state in neighbors.items():
                if state not in explored_states:
                    neighbor = grid.get_node(pos=state)
                    neighbor.parent = node

                    # Calculate h-score
                    h_score = GreedyBestFirstSearch.heuristic(state, grid.end)

                    neighbor.estimated_distance = h_score

                    neighbor.action = action
                    frontier.add(node=neighbor, priority=h_score)

        return NoSolution([], explored_states=list(explored_states))
    
    @staticmethod
    def heuristic(state: tuple[int, int], goal: tuple[int, int]) -> int:
        """Heuristic function for estimating remaining distance

        Args:
            state (tuple[int, int]): current position
            goal (tuple[int, int]): final position
        
        Returns:
            int: Estimated remaining distance from state to goal
        """
        x1, y1 = state 
        x2, y2 = goal 

        return abs(x1 - x2) + abs(y1 - y2)