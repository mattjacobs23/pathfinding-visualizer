from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from .search import BasicSearch

class AStarSearch(BasicSearch):
    @staticmethod 
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search
        
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
            priority=(0 + AStarSearch.heuristic(grid.start, grid.end))
        )
        # f = g + h
        # f -> total estimated distance. The priority
        # g -> distance from start to this node
        # h -> heuristic, estimated distance from this node to goal

        # Keep track of G scores
        g_scores = {grid.start: 0}
        f_scores = {grid.start: AStarSearch.heuristic(grid.start, grid.end)}

        # keep track of explored positions
        explored_states = set() 

        while not frontier.is_empty():
            # Remove node from the frontier
            node = frontier.remove()
            # Add current node position to explored set
            explored_states.add(node.state)

            # Check if this is the destination point
            if node.state == grid.end:
                path, path_cost = AStarSearch.generate_path(node, grid)
                return Solution(path=path,
                                explored_states=list(explored_states),
                                path_cost=path_cost
                                )
            
            # Explore neighbors
            neighbors = grid.get_neighbors(node.state)
            for action, state in neighbors.items():
                # Calculate g-score for this neighbor
                g_score = g_scores[node.state] + grid.get_cost(state)

                if state not in explored_states or g_score < g_scores[state]:
                    # Store the g-score
                    g_scores[state] = g_score

                    # Calculate h-score
                    h_score = AStarSearch.heuristic(state, grid.end)

                    # Calculate f-score
                    f_score = g_score + h_score
                    f_scores[state] = f_score 

                    neighbor = grid.get_node(pos=state)
                    neighbor.parent = node 
                    neighbor.estimated_distance = h_score

                    neighbor.action = action

                    frontier.add(node=neighbor, priority=f_score)
        
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






