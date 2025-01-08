from heapq import heappush, heappop 
from collections import deque

from .node import Node 

class Frontier: 
    """Model a frontier for managing nodes"""

    def __init__(self) -> None:
        self.frontier: list[Node] = []
    
    def add(self, node: Node) -> None:
        """Add a new node to the frontier
        
        Args:
            node (Node): Maze node to add. 
        """
        self.frontier.append(node)
    
    def contains_state(self, state: tuple[int, int]) -> bool:
        """Check if a state exists in the frontier

        Args:
            state (tuple[int, int]): Position of a node

        Returns:
            bool: Whether the provided state exists in the frontier.
        """
        return any(node.state == state for node in self.frontier)

    def is_empty(self) -> bool:
        """Check if the frontier is empty

        Returns:
            bool: Whether the frontier is empty
        """
        return len(self.frontier) == 0


class PriorityQueueFrontier(Frontier):
    def __init__(self) -> None:
        self.frontier: list[tuple[int, Node]] = [] 
    
    def add(self, node: Node, priority: int = 0) -> None:
        """Add a new node to the frontier
        
        Args:
            node (AStarNode): Maze node to add. 
            priority (int, optional): Node priority. Defaults to 0. 
        """
        heappush(self.frontier, (priority, node))
    
    def remove(self) -> Node:
        """Remove a node from the frontier

        Returns:
            AStarNode: Node with lowest f-cost
        """
        _, node = heappop(self.frontier)
        return node

    def get(self, state: tuple[int, int]) -> Node | None:
        """Check if node in frontier. Return node if present, 
        otherwise, return None. 

        Args:
            state (tuple[int, int]): state (position) of the node 
        
        Returns:
            Node: required node
        """
        for _, node in self.frontier:
            if node.state == state:
                return node 
            
        return None

class StackFrontier(Frontier):
    def remove(self) -> Node:
        """Remove element from the stack

        Raises:
            Exception: Empty Frontier
        
        Returns:
            Node: Cell (Node) in the matrix
        """
        if self.is_empty():
            raise Exception("Empty StackFrontier")
        else:
            return self.frontier.pop()


class QueueFrontier(Frontier):
    def __init__(self) -> None:
        self.frontier = deque()
        
    def remove(self) -> Node:
        """Remove element from the queue

        Raises:
            Exception: Empty Frontier
        
        Returns:
            Node: Cell (Node) in the matrix
        """
        if self.is_empty():
            raise Exception("Empty QueueFrontier")
        else:
            return self.frontier.popleft()






