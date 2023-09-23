class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.nodes = [(x, y) for x in range(1, cols + 1) for y in range(1, rows + 1)]

    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        
        # Define the possible movement directions (up, down, left, right)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            neighbor_x, neighbor_y = x + dx, y + dy
            if 1 <= neighbor_x <= self.cols and 1 <= neighbor_y <= self.rows:
                neighbors.append((neighbor_x, neighbor_y))
        
        return neighbors

# Create a grid with the specified number of rows and columns
grid = Grid(30, 52)

