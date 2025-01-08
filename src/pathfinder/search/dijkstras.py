from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from .search import BasicSearch

class DijkstrasSearch(BasicSearch):
    @staticmethod 
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Dijkstras Shortest Path Algorithm
        
        Args:
            grid (Grid): Grid of points
        
        Returns:
            Solution: Solution found
        """
        # Create node for the start cell
        start = grid.get_node(pos=grid.start)

        # Instantiate PriorityQueue frontier and add start node into it
        frontier = PriorityQueueFrontier()
        frontier.add(start)
        
        # Keep track of G scores
        g_scores = {grid.start: 0}

        # Keep track of explored positions
        explored_states = set()

        while not frontier.is_empty():
            # Remove node from the frontier
            node = frontier.remove()

            # Check if this is the destination point
            if node.state == grid.end:
                path, path_cost = DijkstrasSearch.generate_path(node, grid)
                return Solution(path=path,
                                explored_states=list(explored_states),
                                path_cost=path_cost
                                )
            
            if node.state in explored_states:
                continue

            # Add current node position to explored set
            explored_states.add(node.state)
            
            # Explore neighbors
            neighbors = grid.get_neighbors(node.state)
            for action, state in neighbors.items():
                # Calculate g-score for this neighbor
                g_score = g_scores.get(node.state) + grid.get_cost(state)

                if state not in explored_states or g_score < g_scores[state]:
                    # Store the g-score
                    g_scores[state] = g_score

                    neighbor = grid.get_node(pos=state)
                    neighbor.parent = node
                    neighbor.action = action
                    frontier.add(node=neighbor, priority=g_score)

        return NoSolution([], explored_states=list(explored_states))
        
            

