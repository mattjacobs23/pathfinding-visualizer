from typing import Optional
import pygame 

from .pathfinder.models.node import Node
from .animations import AnimatingNode, Animation, AnimationCallback, Animator
from .generate import MazeGenerator, GenerationCallback
from .pathfinder.models.solution import Solution
from .pathfinder.main import PathFinder
from .pathfinder.models.grid import Grid
from .pathfinder.models.search_types import Search

from .constants import * 


class MazeNode(Node):
    def __init__(self,
        value: str,
        state: tuple[int, int],
        cost: int,
        parent: Node | None = None,
        action: str | None = None,
        color: tuple[int, int, int] = WHITE
    ) -> None:
        super().__init__(value, state, cost, parent, action)
        self.color = color 


class Maze: 
    def __init__(self, surface: pygame.surface.Surface) -> None:
        self.surface = surface 
        self.animator: Animator 
        self.generator: MazeGenerator 

        self.width = MAZE_WIDTH // CELL_SIZE 
        self.height = MAZE_HEIGHT // CELL_SIZE

        self.maze = [[MazeNode("1", (row, col), 1)
                for col in range(self.width)]
            for row in range(self.height)]
        
        start_col = self.width // 4 
        goal_col = self.width - (self.width // 4) - 1 

        self.start = (self.height // 2, start_col) # (row, column) 
        self.goal = (self.height // 2, goal_col)
        self.maze[self.start[0]][self.start[1]].value = "A" 
        self.maze[self.start[0]][self.start[1]].cost = 0
        self.maze[self.goal[0]][self.goal[1]].value = "B" 
        self.maze[self.goal[0]][self.goal[1]].cost = 1

        # Generate screen coordinates for maze
        self.coords = self._generate_coordinates() 

        self.speed = "Fast"
    
    def _generate_coordinates(self) -> list[list[tuple[int, int]]]: 
        """Generate screen coordinates for maze

        Returns:
            list[list[tuple[int, int]]]: Coordinate matrix
        """

        coords = []

        # Generate coordinates for every cell in maze matrix

        for i in range(self.height):
            row = []
            for j in range(self.width): 
                # Calculate coordinates for the cell
                x = j * CELL_SIZE + (REMAINDER_W // 2)
                y = i * CELL_SIZE + HEADER_HEIGHT 

                row.append((x,y))

            coords.append(row)

        return coords


    def get_cell_value(self, pos: tuple[int, int]) -> str:
        """Get cell value

        Args:
            pos (tuple[int, int]): Position of the cell
        
        Returns:
            str: Cell value
        """
        return self.maze[pos[0]][pos[1]].value
    

    def get_node(self, pos: tuple[int, int]) -> MazeNode:
        """Get cell node

        Args:
            pos (tuple[int, int]): Position of the cell
        
        Returns:
            MazeNode: Required node
        """
        return self.maze[pos[0]][pos[1]]
    

    def set_cell(self, pos: tuple[int, int], value: str, forced: bool = False) -> None:
        """Update a cell value in the maze

        Args:
            pos (tuple[int, int]): Position of the cell
            value (str): String value for the cell
            forced (bool): Whether or not to force set
        """
        row, col = pos[0], pos[1] 
        if pos in (self.start, self.goal) and not forced:
            if value == "V": 
                self.maze[row][col].color = BLUE 
            elif value == "*":
                self.maze[row][col].color = YELLOW
            return 
        
        match value: 
            case "A": 
                color = WHITE
                cost = 0 
                self.start = pos 
                self.maze[row][col].parent = None
            case "B": 
                color = WHITE
                cost = 1 
                self.goal = pos 
                self.maze[row][col].parent = None
            case "#":
                color = DARK
                cost = -1 
            case "V":
                color = BLUE 
                cost = self.maze[row][col].cost 
            case "*":
                color = YELLOW 
                cost = self.maze[row][col].cost
            case _:
                color = WHITE 
                cost = int(value) 
        
        self.maze[row][col].value = value 
        self.maze[row][col].cost = cost 
        self.maze[row][col].color = color

    def set_speed(self, speed_str: str) -> None:
        if speed_str not in {"Fast", "Medium", "Slow"}:
            return
        self.speed = speed_str

    def clear_board(self) -> None:
        """Clear maze walls
        """
        self.maze = [[MazeNode("1", (row, col), 1)
                for col in range(self.width)]
            for row in range(self.height)]
        
        self.set_cell(self.start, "A", forced=True)
        self.set_cell(self.goal, "B", forced=True)

    def clear_visited(self) -> None: 
        """Clear visited nodes
        """
        for r in range(self.height):
            for c in range(self.width):
                node = self.maze[r][c]
                value = str(node.cost) if node.value in ("V", "*") else node.value
                self.maze[r][c] = MazeNode(
                    value=value,
                    state=(r, c),
                    cost=node.cost
                )

                self.set_cell((r, c), value)

        self.set_cell(self.start, "A", forced=True)
        self.set_cell(self.goal, "B", forced=True)

    def mouse_within_bounds(self, pos: tuple[int, int]) -> bool:
        """Check if mouse cursor is inside the maze

        Args:
            pos (tuple[int, int]): Mouse position
        
        Returns:
            bool: Whether mouse is within the maze
        """
        return all((
            pos[0] > REMAINDER_W // 2,
            pos[0] < WIDTH - REMAINDER_W // 2,

            pos[1] > HEADER_HEIGHT, 
            pos[1] < HEIGHT - REMAINDER_H
        ))

    def get_cell_pos(self, pos: tuple[int, int]) -> tuple[int, int]: 
        """Get cell position from mouse
        
        Args:
            pos (tuple[int, int]): Mouse position
        
        Returns: 
            tuple[int, int]: Cell position
        """
        x, y = pos 
        return (
            (y - HEADER_HEIGHT) // CELL_SIZE, 
            (x - REMAINDER_W // 2) // CELL_SIZE
        )

    def draw(self) -> None:
        """Draw maze"""
        nodes_to_animate = self.animator.nodes_to_animate 

        # Draw every cell on the screen
        for r, row in enumerate(self.maze):
            for c, node in enumerate(row):
                x, y = self.coords[r][c]
                center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)

                if not center in nodes_to_animate: 
                    self._draw_rect((r, c), node.color)
                    continue 

                # center is in nodes_to_animate 
                for k in range(len(nodes_to_animate[center]) - 1, -1, -1):
                    animating_node = nodes_to_animate[center][k]
                    if animating_node.progress > 0:
                        self._draw_rect(
                            coords=(r, c),
                            color=animating_node.color,
                            node=animating_node
                        )
                        break 
                else:
                    self._draw_rect((r,c), node.color)
        
    def generate_maze(
            self, 
            algorithm: str,
            after_generation: Optional[GenerationCallback] = None
    ) -> None:
        """Generate maze using an algorithm

        Args:
        algorithm (str): Algorithm name
        """

        match algorithm:
            case "Basic Random Maze":
                self.generator.basic_random_maze() 
            case "Basic Weight Maze":
                self.generator.basic_weight_maze()
            case "Randomized DFS":
                self.generator.randomized_dfs()
            case "Prim's Algorithm":
                self.generator.randomized_prims_algorithm()
            case "Recursive Division":
                self._draw_walls_around()
                self.generator.recursive_division(1, self.width - 2, 1, self.height - 2)
        
        animate_values_list = list(self.animator.nodes_to_animate.values())
        try:
            animate_values_list[-1][-1].after_animation = after_generation
        except Exception as e:
            print(e, self.animator.nodes_to_animate)
            raise
            

    def _draw_walls_around(self) -> None:
        """Draw walls around the maze
        """
        # combine top and bottom horizontal actually:
        # Top Horizontal
        nodes_to_animate = []
        for i in range(self.width):
            x, y = self.coords[0][i]
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)

        # Bottom horizontal
        nodes_to_animate = []
        for i in range(self.width):
            x, y = self.coords[-1][i]
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)

        # Sides
        nodes_to_animate = []
        for i in range(self.height):
            x, y = self.coords[i][0]
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

            x, y = self.coords[i][-1]
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)
    
    def solve(self, algo_name: str,) -> Solution:
        """Solve the maze with an algorithm

        Args:
            algo_name (str): Name of algorithm
        """
        # String -> Search Algorithm
        mapper: dict[str, Search] = {
            "A* Search": Search.ASTAR_SEARCH,
            "Dijkstra's Search": Search.DIJKSRAS_SEARCH,
            "Greedy Best First Search": Search.GREEDY_BEST_FIRST_SEARCH,
            "Breadth First Search": Search.BREADTH_FIRST_SEARCH,
            "Depth First Search": Search.DEPTH_FIRST_SEARCH,
        }

        # Instantiate Grid for PathFinder
        grid = Grid(self.maze, self.start, self.goal)  # type: ignore

        # Solve the maze
        solution = PathFinder.find_path(
            grid=grid,
            search_type=mapper[algo_name.strip()],
        )

        return solution

    def visualize(
        self,
        solution: Solution,
        after_animation: Optional[AnimationCallback] = None,
    ) -> None:
        """Visualize solution

        Args:
            solution (Solution): Solution object
            after_animation (Optional[AnimationCallback], optional): Called after animation. Defaults to None.
        """

        # Animate solution nodes
        nodes = []
        for cell in solution.explored_states:
            x, y = self.coords[cell[0]][cell[1]]
            nodes.append(
                AnimatingNode(
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    rect=pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE),
                    ticks=pygame.time.get_ticks(),
                    value="V",
                    color=WHITE,
                    colors=[YELLOW, DARK_BLUE_2, BLUE_2, GREEN_2, BLUE],
                    duration=1500,
                    animation=Animation.PATH_ANIMATION
                )
            )

        match self.speed:
            case "Fast":
                gap = 5
            case "Medium":
                gap = 30
            case "Slow":
                gap = 1000
            case _:
                gap = 5

        self.animator.add_nodes_to_animate(nodes, gap=gap)

        if not solution.path:
            nodes[-1].after_animation = after_animation
            return

        # Color the shortest path in yellowd
        nodes = []
        for cell in solution.path:
            x, y = self.coords[cell[0]][cell[1]]
            nodes.append(
                AnimatingNode(
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                    ticks=pygame.time.get_ticks(),
                    value="*",
                    color=YELLOW,
                    duration=1000,
                )
            )

        match gap:
            case 5:
                gap = 30
            case 30:
                gap = 50
            case 1000:
                gap = 50

        self.animator.add_nodes_to_animate(nodes, delay=600, gap=gap)
        nodes[-1].after_animation = after_animation
    

    def _draw_rect(
            self,
            coords: tuple[int, int],
            color: tuple[int, int, int] = BLUE,
            node: AnimatingNode | None = None
    ) -> None:
        """Color an existing cell in the maze

        Args:
            coords (tuple[int, int]): Cell coordinates
            color (tuple[int, int, int], optional): Color. Defaults to YELLOW.
            node (AnimatingNode, optional): The animating node to draw. Defaults to None. 
        """

        # Determine maze coordinates
        row, col = coords
        x, y = self.coords[row][col]

        if coords in (self.start, self.goal) and color == DARK:
            return

        # Draw
        pygame.draw.rect(
            surface=self.surface,
            color=color,
            rect=node.rect if node else pygame.Rect(
                x, y, CELL_SIZE, CELL_SIZE)
        )

        # Draw border if needed
        if color in (BLUE, WHITE, GREEN) or \
                (node and node.color == YELLOW):
            pygame.draw.rect(
                surface=self.surface,
                color=GREEN if color == GREEN_2 else GRAY,
                rect=pygame.Rect(x, y, CELL_SIZE, CELL_SIZE),
                width=1
            )

        # Draw images if needed
        if (n := self.maze[row][col]).cost > 1:
            image_rect = WEIGHT.get_rect(
                center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            self.surface.blit(WEIGHT, image_rect)

            text = FONT_14.render(
                str(n.cost if not node else node.value), True, GRAY
            )
            text_rect = text.get_rect()
            text_rect.center = image_rect.center
            self.surface.blit(text, text_rect)

        elif (row, col) == self.start:
            image_rect = START.get_rect(
                center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            self.surface.blit(START, image_rect)

        elif (row, col) == self.goal:
            image_rect = GOAL.get_rect(
                center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            self.surface.blit(GOAL, image_rect)
 


                

                









        