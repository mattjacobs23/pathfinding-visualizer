from enum import Enum 

class Search(Enum):
    """Enum for search algorithms"""

    DEPTH_FIRST_SEARCH = "DFS"
    BREADTH_FIRST_SEARCH = "BFS"
    ASTAR_SEARCH = "A*"
    GREEDY_BEST_FIRST_SEARCH = "GBFS"
    DIJKSRAS_SEARCH = "DS"