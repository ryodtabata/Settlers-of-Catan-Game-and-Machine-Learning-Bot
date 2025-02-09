import pygame
import math
import random
from classtypes import *



# Screen Dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settlers of Catan Board")

# Hexagon Size
HEX_SIZE = 60
CLICK_RADIUS = 10
turn_ended = False
# Colors
# update colour later, with pictures
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)

# Load images for each resource
WOOD_IMAGE = pygame.image.load("images/wood.jpeg")
BRICK_IMAGE = pygame.image.load("images/brick.jpeg")
WHEAT_IMAGE = pygame.image.load("images/wheat.jpg")
SHEEP_IMAGE = pygame.image.load("images/sheep.jpeg")
ORE_IMAGE = pygame.image.load("images/ore.jpeg")
DESERT_IMAGE = pygame.image.load("images/desert.jpeg")

# Dictionary mapping resources to their images
RESOURCE_IMAGES = {
    "wood": WOOD_IMAGE,
    "brick": BRICK_IMAGE,
    "wheat": WHEAT_IMAGE,
    "sheep": SHEEP_IMAGE,
    "ore": ORE_IMAGE,
    "desert": DESERT_IMAGE,
}

RESOURCES_COLORS = {
    "wood": GREEN,
    "brick": RED,
    "sheep": WHITE,
    "wheat": YELLOW,
    "ore": GRAY,
    "desert": (210, 180, 140),
}

TOUCHING_HEXIGONS = {
    0: [1, 3, 4],          # Top left corner
    1: [0, 2, 4, 5],       # Top middle
    2: [1, 5, 6],          # Top right corner
    3: [0, 4, 7, 8],       # Second row, left
    4: [0, 1, 3, 5, 8, 9], # Second row, middle
    5: [1, 2, 4, 6, 9, 10],# Second row, right
    6: [2, 5, 10, 11],     # Third row, right
    7: [3, 8, 12],         # Third row, left
    8: [3, 4, 7, 9, 12, 13],# Third row, middle left
    9: [4, 5, 8, 10, 13, 14],# Third row, middle right
    10: [5, 6, 9, 11, 14, 15],# Third row, right
    11: [6, 10, 15],       # Bottom right corner
    12: [7, 8, 13, 16],    # Bottom row, left
    13: [8, 9, 12, 14, 16, 17],# Bottom row, middle left
    14: [9, 10, 13, 15, 17, 18],# Bottom row, middle right
    15: [10, 11, 14, 18],  # Bottom row, right
    16: [12, 13, 17],      # Bottom left corner
    17: [13, 14, 16, 18],  # Bottom middle
    18: [14, 15, 17]       # Bottom right corner
}

LAYOUT = layout = [
    (-2, 2), (0, 2), (2, 2),        # Top row
    (-3, 1), (-1, 1), (1, 1), (3, 1),  # Second row
    (-4, 0), (-2, 0), (0, 0), (2, 0), (4, 0),  # Middle row
    (-3, -1), (-1, -1), (1, -1), (3, -1),  # Fourth row
    (-2, -2), (0, -2), (2, -2)     # Bottom row
]

def hex_mask(size):
    """Creates a hexagonal mask surface."""
    mask = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))  # Transparent background

    hex_points = [
        (
            size + size * math.cos(math.pi / 6 + i * math.pi / 3),
            size + size * math.sin(math.pi / 6 + i * math.pi / 3)
        )
        for i in range(6)
    ]

    pygame.draw.polygon(mask, (255, 255, 255, 255), hex_points)  # White hexagon
    return mask

# Create Tiles
def create_tiles():
    resources = ['wood'] * 4 + ['brick'] * 3 + ['sheep'] * 4 + ['wheat'] * 4 + ['ore'] * 3 + ['desert']
    numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    random.shuffle(resources)
    random.shuffle(numbers)

    tiles = []
    for resource in resources:
        if resource == "desert":
            tiles.append(HexTile(resource, None))
        else:
            tiles.append(HexTile(resource, numbers.pop()))
    
    return tiles

#give position for each hexigon, so we know where it is on the board
def hex_cords(tiles):
    for tile, (grid_x, grid_y) in zip(tiles, LAYOUT):
        # Calculate pixel coordinates for the hexagon center
        x_center = WIDTH // 2 + grid_x * HEX_SIZE * .85
        y_center = HEIGHT // 2 - grid_y * HEX_SIZE * 1.45
        # Add x_center and y_center to the tile object
        tile.xcenter = x_center
        tile.ycenter = y_center
    return True

def is_within_threshold(coord1, coord2, threshold):
    """Check if two coordinates are within the given threshold."""
    return abs(coord1[0] - coord2[0]) < threshold and abs(coord1[1] - coord2[1]) < threshold

def create_vertex_for_hex(tiles):
    """
    Returns:
        hex_to_verts: Dictionary mapping tile numbers to their vertex IDs.
        vertices: Dictionary mapping vertex IDs to Vertex objects.
    """

    vert_id = 0
    vertices = {}  # {vertex_id: Vertex}
    vertex_positions = {}  # {(x, y): vertex_id}
    hex_to_verts = {}  # {tile_number: {resource: [vertex_ids]}}
    THRESHOLD = 10

    for tile in tiles:
        if tile.number not in hex_to_verts:
            hex_to_verts[tile.number] = {}  # Initialize the nested dictionary for this tile

        if tile.resource not in hex_to_verts[tile.number]:
            hex_to_verts[tile.number][tile.resource] = []  # Initialize the vertex list for the resource

        # Loop through 6 vertices of the hexagon
        for i in range(6):
            angle = math.pi / 6 + 2 * math.pi / 6 * i  # Calculate vertex angle
            vertex_x = tile.xcenter + HEX_SIZE * math.cos(angle)
            vertex_y = tile.ycenter + HEX_SIZE * math.sin(angle)

            # Snap the vertex to a grid to avoid floating-point precision issues
            vertex_coords = (round(vertex_x, 2), round(vertex_y, 2))

            # Check if this vertex is close enough to an existing one
            close_vertex_id = None

            for existing_coords, existing_id in vertex_positions.items():
                if is_within_threshold(vertex_coords, existing_coords, THRESHOLD):
                    close_vertex_id = existing_id
                    break

            if close_vertex_id is None:
                # Create a new Vertex
                new_vertex = Vertex(vert_id, vertex_coords)
                vertices[vert_id] = new_vertex
                vertex_positions[vertex_coords] = vert_id
                hex_to_verts[tile.number][tile.resource].append(vert_id)
                vert_id += 1
            else:
                # Reuse the existing vertex ID
                hex_to_verts[tile.number][tile.resource].append(close_vertex_id)
    return hex_to_verts, vertices, vertex_positions

#makes the board
def make_board(screen, board):
    """
    Draw the Settlers of Catan board on the screen with masked images inside hexagons.
    """
    screen.fill((200, 200, 200))  # Background color

    for tile in board.tiles:
        x_center = tile.xcenter
        y_center = tile.ycenter

        # Get the image and resize it
        tile_image = RESOURCE_IMAGES[tile.resource]
        tile_image = pygame.transform.scale(tile_image, (HEX_SIZE * 2, HEX_SIZE * 2))

        # Create a hexagonal mask
        mask = hex_mask(HEX_SIZE)

        # Apply the mask to the image
        tile_surface = pygame.Surface((HEX_SIZE * 2, HEX_SIZE * 2), pygame.SRCALPHA)
        tile_surface.blit(tile_image, (0, 0))
        tile_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Blit the masked image onto the screen
        screen.blit(tile_surface, (x_center - HEX_SIZE, y_center - HEX_SIZE))

        # Draw hexagon border
        hex_points = [
            (
                x_center + HEX_SIZE * math.cos(math.pi / 6 + i * math.pi / 3),
                y_center + HEX_SIZE * math.sin(math.pi / 6 + i * math.pi / 3)
            )
            for i in range(6)
        ]
        pygame.draw.polygon(screen, (0, 0, 0), hex_points, 2)

        # Draw tile number
        font = pygame.font.Font(None, 50)
        desert_font = pygame.font.Font(None, 30)
        if tile.resource != "desert":
            text = font.render(f"{tile.number}", True, WHITE)
        else:
            text = desert_font.render("DESERT", True, WHITE)
        text_rect = text.get_rect(center=(x_center, y_center))
        screen.blit(text, text_rect)

        for vertex_id, vertex in board.vertices.items():
            x, y = vertex.cords
            # Draw the vertex as a small circle
            pygame.draw.circle(screen, WHITE, (int(x), int(y)), 5)  

            if vertex.owner=="player1": 
                color = RED
            elif vertex.owner =="player2":
                color= GREEN
            elif vertex.owner =="player3":
                color = BLACK
            elif vertex.owner =="player4":
                color= YELLOW
        
            # If a settlement exists, draw it
            if vertex.type == "settlement":
                pygame.draw.circle(screen, color, (int(x), int(y)), 10)
            elif vertex.type == "city":
                pygame.draw.circle(screen, color, (int(x), int(y)), 12)

        for edge in board.edges:
            x1, y1 = edge.vertex1.cords
            x2, y2 = edge.vertex2.cords
            if edge.owner:  # Only draw if owned
                if edge.owner=="player1": 
                    color = RED
                elif edge.owner =="player2":
                    color= GREEN
                elif edge.owner =="player3":
                    color = BLACK
                elif edge.owner =="player4":
                    color= YELLOW
                pygame.draw.line(screen, color, (x1, y1), (x2, y2), 5)  # Thick road
    pygame.display.flip()

#checks all the hexigons to ensure the board is valid, no 6s or 8s next to eachother
def validcheck(tiles):
    for tilenum in range(19):
        if tiles[tilenum].number == 6 or tiles[tilenum].number == 8:
            #adjacent tiles check
            adj = TOUCHING_HEXIGONS[tilenum]
            for hexigon in adj:
                if tiles[hexigon].number == 6 or tiles[hexigon].number == 8:
                    return True      
    return False

#rolls two die and returns sum
def rolldice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return die1+die2

def make_unbuildable(cords, vertex_positions, board, radius=80):
    """
    Marks vertices within a given radius as unbuildable.
    
    Parameters:
    - cords: The center position (x, y) around which to create the unbuildable circle.
    - vertex_positions: Dictionary of vertex positions {vertex: (x, y)}.
    - board: The game board object that contains vertex properties.
    - radius: The radius of the circle within which vertices become unbuildable.
    """
    for position, vertex in vertex_positions.items():
        # Calculate the Euclidean distance from the center to each vertex
        distance = math.sqrt((cords[0] - position[0])**2 + (cords[1] - position[1])**2)
        
        # If the distance is less than or equal to the radius, mark it as unbuildable
        if distance <= radius:
            board.vertices[vertex].buildable = False

#function that creates the first 2 settlements and roads
def initialsetup(event, players, board, turns, vertex_positions,screen):
    """
    Handles the initial setup phase for placing settlements.
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        cords = event.pos
        for position, vertex in vertex_positions.items():
            # Calculate the distance between the click and the vertex
            distance = math.sqrt((cords[0] - position[0])**2 + (cords[1] - position[1])**2)
            if distance <= CLICK_RADIUS:
                if board.vertices[vertex].buildable==True:
                    current_player = players[turns.pop(0)]
                    current_player.build_settlement(board, vertex)  #ent
                    make_unbuildable(cords,vertex_positions,board)
                    make_board(screen,board)
                    first_road(board,current_player,vertex_positions,vertex)
                    make_board(screen,board)
                if turns!= []:
                    return False
                else:
                    return True
    return False


#helper fucntion for the first roads
def first_road(board, current_player, vertex_positions, target_vertex):
    running = True
    verts = board.adj_matrix[target_vertex]
    while running:
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cords = event.pos
                    for position, vertex in vertex_positions.items():
            # Calculate the distance between the click and the vertex
                        distance = math.sqrt((cords[0] - position[0])**2 + (cords[1] - position[1])**2)
                        if distance <= CLICK_RADIUS and vertex in verts:
                            edge = Edge(board.vertices[target_vertex],board.vertices[vertex],current_player.name)
                            board.edges.append(edge)
                            running = False 

def is_adjacent(board, v1, v2):
    return v2 in board.adj_matrix.get(v1, [])

#distrributes all the resources for each roll
def distribute_rrs(roll,board,hex_to_verts,players):
    if roll == 7:
        return True
    for tile in hex_to_verts[roll]:
        for vertex in hex_to_verts[roll][tile]:
            if board.vertices[vertex].type=="settlement":
                name = board.vertices[vertex].owner
                for player in players:
                    if player.name == name and tile in player.resources:
                        player.resources[tile]+=1
                    elif player.name == name:
                        player.resources[tile] = 1
                        
            elif board.vertices[vertex].type=="city":
                name = board.vertices[vertex].owner
                for player in players:
                    if player.name == name and tile in player.resources:
                        player.resources[tile]+=2
                    elif player.name == name:
                        player.resources[tile]=2
    return True

def maketurn(board, players, screen,vertex_positions):
    global turn_ended
    buttons = HUD(board, players, screen,vertex_positions)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        button.action()  # Execute the button action
                        HUD(board, players, screen,vertex_positions)
        
                        
        if turn_ended:
            # Logic to proceed to the next turn goes here
            print("next turn.")
            turn_ended = False  # Reset the flag for the next turn
            return True


def reachable(board,player,vertex):
    for edge in board.edges:
        if edge.owner==player.name:
          
            if vertex == edge.vertex1.id or vertex == edge.vertex2.id:
                return True
    return False


def build_settlement(board,player,vertex_positions):
    # rrs = ['wheat','sheep','brick','wood']
    # for r in rrs:
    #     if r not in player.resources:
    #         print("does not have")
    #         return 
    #     elif player.resources[r]<1:
    #         print("cannot afford")
    #         return

    while True:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                for position, vertex in vertex_positions.items():
                # Calculate the distance between the click and the vertex
                    distance = math.sqrt((cords[0] - position[0])**2 + (cords[1] - position[1])**2)
                    if distance <= CLICK_RADIUS:
                        if board.vertices[vertex].buildable==True and reachable(board,player,vertex):
                            player.build_settlement(board, vertex)  #ent
                            make_unbuildable(cords,vertex_positions,board)
                            make_board(screen, board)  # Redraw the board
                            pygame.display.flip()  # Update the display
                            # for r in rrs:
                            #     player.resources[r] = player.resources[r]-1
                            return
                        return
                            
def build_city(board,player):
    return True

def buy_dev_card(board,player):
    return True


def build_road(board, current_player, vertex_positions):
    verts = []
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                print(cords)

                # Find the vertex closest to the mouse click
                for position, vertex in vertex_positions.items():
                    distance = math.sqrt((cords[0] - position[0])**2 + (cords[1] - position[1])**2)
                    
                    if distance <= CLICK_RADIUS:  # The click is within range of a vertex
                        if len(verts) == 0:  # First click, record the vertex
                            if reachable(board, current_player, vertex):
                                verts.append(vertex)
                                print('First vertex reachable:', vertex)
                                break  # Exit the loop after selecting the first vertex
                            else:
                                print("Vertex not reachable.")
                                return  # Return early if the first vertex is not reachable
                        
                        else:  # Second click, check if it's valid
                            if vertex in board.adj_matrix[verts[0]]:  # Check adjacency
                                verts.append(vertex)
                                edge = Edge(board.vertices[verts[0]], board.vertices[verts[1]], current_player.name)
                                board.edges.append(edge)
                                print(f"Road built between {verts[0]} and {verts[1]}")
                                running = False  # Stop the loop after the second vertex is selected and road is built
                                break  # Exit the loop after building the road
                            else:
                                print("Second vertex is not adjacent.")
                                verts.clear()  # Clear the vertex list to allow retrying
                                break  # Exit to start over with a new selection
        make_board(screen,board)
        pygame.display.update()  # Update the display after processing events

    return
        
        

def end_turn(board):
    global turn_ended
    # Only change the turn if the button is clicked
    turn_ended = True
    if board.turn ==4:
        board.turn = 1
    else:
        board.turn +=1
    # Additional logic for ending the turn can go here
    print("Turn has ended.")


def HUD(board, players, screen,vertex_positions):
    """
    Handles a player's turn in Pygame.
    """
    global turn_ended
    turn = board.turn
    if turn==1:
        color = RED
    elif turn ==2:
        color= GREEN
    elif turn ==3:
        color = BLACK
    elif turn==4:
        color= YELLOW

    turn = board.turn - 1 # Adjust for 0-based index
    current_player = players[turn]
 
         
    # Display the player's turn
    font = pygame.font.Font(None, 40)
    turn_text = font.render(f"Player {board.turn}'s Turn", True,color)
    screen.blit(turn_text, (500, 680))

    # Show the player's resources
    y_offset = 80
    font = pygame.font.Font(None, 30)
    for resource, count in current_player.resources.items():
        resource_text = font.render(f"{resource}: {count}", True, (255, 255, 255))
        screen.blit(resource_text, (50, y_offset))
        y_offset += 30

    # Show the player's development cards
    y_offset += 20
    screen.blit(font.render("Development Cards:", True, (255, 255, 255)), (50, y_offset))
    y_offset += 30
    for dev_card in current_player.dev_cards:
        dev_text = font.render(f"- {dev_card}", True, (255, 255, 255))
        screen.blit(dev_text, (50, y_offset))
        y_offset += 30

    # Show rewards (Longest Road, Largest Army)
    y_offset += 20
    if board.longest_road == current_player.name:
        screen.blit(font.render("🏆 Longest Road!", True, (255, 255, 0)), (50, y_offset))
        y_offset += 30
    if board.largest_army == current_player.name:
        screen.blit(font.render("🏆 Largest Army!", True, (255, 255, 0)), (50, y_offset))

    # Create action buttons
    buttons = [
        Button(50, 300, 200, 50, "Build Road", (0, 128, 255), lambda: build_road(board, current_player, vertex_positions)),
        Button(50, 360, 200, 50, "Build Settlement", (0, 128, 0), lambda: build_settlement(board, current_player,vertex_positions)),
        Button(50, 420, 200, 50, "Build City", (255, 165, 0), lambda: build_city(board, current_player)),
        Button(50, 480, 200, 50, "Buy Dev Card", (128, 0, 128), lambda: buy_dev_card(board, current_player)),
        Button(50, 540, 200, 50, "End Turn", (255, 0, 0), lambda: end_turn(board))
    ]

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
    return buttons


def main():
    incorrectsetup = True
    while incorrectsetup:
        tiles = create_tiles()
        incorrectsetup = validcheck(tiles)

    hex_cords(tiles)  # Assign coordinates to tiles
    hex_to_verts, vertices, vertex_positions = create_vertex_for_hex(tiles)
    board = Board(tiles, vertices)
    player1 = Player("player1")
    player2 = Player("player2")
    player3 = Player("player3")
    player4 = Player("player4")

    players = [player1, player2, player3, player4]

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Settlers of Catan Board")
    # Initialize the settlement phase
    # Setup state variables


    turns = [0, 1, 2, 3, 3, 2, 1, 0]  # Turn order
    setup_complete = False #change to start game 
    main_game = True #toggle these two to start
    running = True
    make_board(screen, board)  # make board
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not setup_complete:
                setup_complete = initialsetup(event, players, board, turns, vertex_positions,screen)
                main_game = False
            elif not main_game:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Check if the key pressed is the spacebar
                        roll = rolldice()
                        font = pygame.font.Font(None, 70)
                        turn_text = font.render(f"{roll} rolled", True, BLACK)
                        screen.blit(turn_text, (50, 20))
                        distribute_rrs(roll,board,hex_to_verts,players)
                        maketurn(board,players,screen,vertex_positions)            
        make_board(screen, board)  # Redraw the board
        pygame.display.flip()  # Update the display


if __name__ == "__main__":
    main()


#THINGS THAT NEED TO BE DONE:   
# BUILDING ROADS, 
# SETTLEMTNS, check if is connected via road 
# CITIES, 
# IMPLEMENT DEV CARDS, 
# ENSURE FIRST ROAD MUST BE BUILD ATTACHED TO SETTLEMENT, 
# roads build on top of eachoehtre 
