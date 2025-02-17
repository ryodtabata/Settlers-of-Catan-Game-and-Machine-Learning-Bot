import pygame
import math
import random
from classtypes import *

# Screen Dimensions

WIDTH, HEIGHT = 1200, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settlers of Catan Board")
pygame.font.init()
# Hexagon size
HEX_SIZE = 60
CLICK_RADIUS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Constants for sidebar
SIDEBAR_WIDTH = 250  # Adjust as needed
BUTTON_MARGIN = 10
BUTTON_WIDTH = 230
BUTTON_HEIGHT = 40
SECTION_SPACING = 20  # Space between sections

PLAYER_DIC = {'player1':0,'player2':1,'player3':2,'player4':3}


#load images for each resource
WOOD_IMAGE = pygame.image.load("images/wood.jpeg")
BRICK_IMAGE = pygame.image.load("images/brick.jpeg")
WHEAT_IMAGE = pygame.image.load("images/wheat.jpg")
SHEEP_IMAGE = pygame.image.load("images/sheep.jpeg")
ORE_IMAGE = pygame.image.load("images/ore.jpeg")
DESERT_IMAGE = pygame.image.load("images/desert.jpeg")
#dictionary mapping resources to their images

#for each vertex, shows which 
ADJ_MATRIX = {
        # Row 1 (Hexagon 1: vertices 4, 5, 0, 1, 2, 3)
        4: [5, 3],
        5: [4, 8,0],
        0: [5, 7,1],
        1: [0,14,2],
        2: [1,3,17],
        3: [4,2],

        # Row 2 (Hexagon 2: vertices 6, 7, 8, 9, 10, 11)
        6: [9,11,7],
        7: [0,6,18],
        8: [9,5],
        9: [8,12,6],
        10: [13,11,24],
        11: [6,10,20],
        #here
        # Row 3 (Hexagon 3: vertices 12, 13, 14, 15, 16, 17)
        12: [9,13],
        13: [12,10],
        14: [1,15,19],
        15: [16,14,25],
        16: [28,15,17],
        17: [2,16],

        # Row 4 (Hexagon 4: vertices 18, 19, 20, 21, 22, 23)
        18: [7,19,21],
        19: [18,14,29],
        20: [11,21,23],
        21: [20,18,31],
        22: [23,24,37],
        23: [20,22,33],

        # Row 5 (Hexagon 5: vertices 24, 25, 26, 27, 28, 29)
        24: [10,22],
        25: [30,26,15],
        26: [27,25,40],
        27: [28,26],
        28: [16,27],
        29: [19,30,32],

        # Row 6 (Hexagon 6: vertices 30, 31, 32, 33, 34, 35)
        30: [25,29,38],
        31: [21,32,34],
        32: [29,31,41],
        33: [34,36,23],
        34: [31,33,43],
        35: [37,36],

        # Row 7 (Hexagon 7: vertices 36, 37, 38, 39, 40, 41)
        36: [33,35,45],
        37: [22,35],
        38: [30,39,42],
        39: [40,38,49],
        40: [26,39],
        41: [32,42,44],

        # Row 8 (Hexagon 8: vertices 42, 43, 44, 45, 46, 47)
        42: [38,41,47],
        43: [34,44,46],
        44: [41,43,50],
        45: [36,46],
        46: [43,45,52],
        47: [42,48,51],

        # Row 9 (Hexagon 9: vertices 48, 49, 50, 51, 52, 53)
        48: [47,49],
        49: [39,48],
        50: [51,44,53],
        51: [47,50],
        52: [46,53],
        53: [50,52],
    }

RESOURCE_IMAGES = {
    "wood": WOOD_IMAGE,
    "brick": BRICK_IMAGE,
    "wheat": WHEAT_IMAGE,
    "sheep": SHEEP_IMAGE,
    "ore": ORE_IMAGE,
    "desert": DESERT_IMAGE,
}

# this is a dictionary, for all of the hexigons and which hexigons they touch, made this to ensure no 8 and 6 are next to eachother
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

#layout for hexigon creation
LAYOUT = [
    (-2, 2), (0, 2), (2, 2),        # Top row
    (-3, 1), (-1, 1), (1, 1), (3, 1),  # Second row
    (-4, 0), (-2, 0), (0, 0), (2, 0), (4, 0),  # Middle row
    (-3, -1), (-1, -1), (1, -1), (3, -1),  # Fourth row
    (-2, -2), (0, -2), (2, -2)     # Bottom row
]

#mask fucntion adds skin to each hexigon (wood,brick,sheep,etc)
def hex_mask(size):
    
    mask = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))  
    hex_points = [
        (
            size + size * math.cos(math.pi / 6 + i * math.pi / 3),
            size + size * math.sin(math.pi / 6 + i * math.pi / 3)
        )
        for i in range(6)
    ]
    pygame.draw.polygon(mask, (255, 255, 255, 255), hex_points)  # White hexagon
    return mask

#give position for each hexigon, so we know where it is on the board
def hex_cords(tiles):
    for tile, (grid_x, grid_y) in zip(tiles, LAYOUT):
        # \pixel coordinates for the hexagon center
        x_center = WIDTH // 2 + grid_x * HEX_SIZE * .85
        y_center = HEIGHT // 2 - grid_y * HEX_SIZE * 1.45
        # Add x_center and y_center to the tile object
        tile.xcenter = x_center
        tile.ycenter = y_center
    return True

#create tiles, tile.robber , tile.resource, tile.number
def create_tiles():
    idnum =0
    resources = ['wood'] * 4 + ['brick'] * 3 + ['sheep'] * 4 + ['wheat'] * 4 + ['ore'] * 3 + ['desert']
    numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    random.shuffle(resources)
    random.shuffle(numbers)

    tiles = []
    for resource in resources:
        if resource == "desert":
            tiles.append(HexTile(resource, None,idnum))
        else:
            tiles.append(HexTile(resource,numbers.pop(),idnum))
        idnum+= 1
    
    return tiles

#checks to see if 
def is_within_threshold(coord1, coord2, threshold):
    """Check if two coordinates are within the given threshold."""
    return abs(coord1[0] - coord2[0]) < threshold and abs(coord1[1] - coord2[1]) < threshold

#returns verticies dictionary, vertID to vertex and hex_to_verts a {} of hexid to verts asscoaited with
def create_vertex_for_hex(tiles):
    vert_id = 0  # Keep track of the vertex IDs
    vertices = {}  # {vertex_id: Vertex} maps a vertex ID to the vertex itself
    vertex_positions = {}  # {(x, y): vertex_id} to check for existing positions
    hexagons_associated_verts = {}  # Maps tile ID to associated vertex IDs

    # Ensure hexagons_associated_verts is initialized
    for tile in tiles:
        hexagons_associated_verts[tile.id] = []

    for tile in tiles:
        for i in range(6):
            # Loop through 6 vertices of the hexagon
            angle = math.pi / 6 + 2 * math.pi / 6 * i  # Calculate vertex angle
            vertex_x = tile.xcenter + HEX_SIZE * math.cos(angle)
            vertex_y = tile.ycenter + HEX_SIZE * math.sin(angle)
            # Snap the vertex to a grid to avoid precision issues
            vertex_coords = (round(vertex_x, 2), round(vertex_y, 2))
            close_vertex_id = None

            # Check if vertex is close to an existing one
            for existing_coords, existing_id in vertex_positions.items():
                if is_within_threshold(vertex_coords, existing_coords, 10):
                    close_vertex_id = existing_id
                    break

            if close_vertex_id is None:
                # Create a new vertex
                new_vertex = Vertex(vert_id, vertex_coords)
                vertices[vert_id] = new_vertex
                vertex_positions[vertex_coords] = vert_id
                hexagons_associated_verts[tile.id].append(vert_id)
                vert_id += 1
            else:
                # Reuse the existing vertex ID
                hexagons_associated_verts[tile.id].append(close_vertex_id)

    return vertices, hexagons_associated_verts

#adds the associated verts to each hexigon
def add_verts_to_each_hex(hex_to_verts,tiles):
    for tile in tiles:
        tile.verts = hex_to_verts[tile.id]
        
#makes the board
def make_board(board):
    """
    Draw the Settlers of Catan board on the screen with masked images inside hexagons.
    """
    SCREEN.fill((200, 200, 200))  # Background color

    #draws all the hexigons, including if its being robber or not 
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
        SCREEN.blit(tile_surface, (x_center - HEX_SIZE, y_center - HEX_SIZE))

        # Draw hexagon border
        hex_points = [
            (
                x_center + HEX_SIZE * math.cos(math.pi / 6 + i * math.pi / 3),
                y_center + HEX_SIZE * math.sin(math.pi / 6 + i * math.pi / 3)
            )
            for i in range(6)
        ]
        pygame.draw.polygon(SCREEN, (0, 0, 0), hex_points, 2)

        # Draw tile number
        font = pygame.font.Font(None, 50)
        desert_font = pygame.font.Font(None, 30)
        if tile.resource != "desert":
            text = font.render(f"{tile.number}", True, BLACK)
        else:
            text = desert_font.render("DESERT", True, BLACK)

        text_rect = text.get_rect(center=(x_center, y_center))
        SCREEN.blit(text, text_rect)

        if tile.robber == True:
            pygame.draw.circle(SCREEN, BLACK, (int(x_center), int(y_center)), 20)

    for vertexid, vertex in board.vertices.items():
        x, y = vertex.cords
        # Draw the vertex as a small circle
        pygame.draw.circle(SCREEN, BLACK, (int(x), int(y)), 3)  

        # If a settlement exists, draw it
        if vertex.type == "settlement":
            pygame.draw.circle(SCREEN, vertex.color, (int(x), int(y)), 10)
        elif vertex.type == "city":
            pygame.draw.circle(SCREEN, vertex.color, (int(x), int(y)), 15)


    for edge in board.edges:
        x1, y1 = edge.vertex1.cords
        x2, y2 = edge.vertex2.cords
        if edge.owner:  # Only draw if owned
            pygame.draw.line(SCREEN, edge.color, (x1, y1), (x2, y2), 5)  # Thick road

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

#rolls two die and returns sum, to ensure random dice
def rolldice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return die1+die2

#for the initial setup of settlements and roads
def initialsetup(players, board, turns):
   #handles initial setup
    while turns:  
        current_player = players[turns[0]]  
        display_message(f"{current_player.name}, please place your settlement!", 62)
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                for vertexid, vertex in board.vertices.items():  #iterate over all vertices
                    if is_close_enough(cords, vertex.cords):
                        if vertex.buildable:
                            current_player.build_settlement(board, vertexid)  
                            make_unbuildable(vertex.cords, board) 
                            make_board(board)
                            first_road(board,current_player,vertexid)
                            make_board(board)
                            turns.pop(0)  
                            break  

                # Check if all players have placed their settlements
                if not turns:
                    print('successful startup')
                    return True  # All players are done, exit function

        pygame.display.flip()  # Update the display

    return False 

#are the cords close enopugh to actual cords?
def is_close_enough(cords, vertex_coords, threshold=30):
    """Check if the mouse click is within a certain threshold distance from the vertex."""
    return math.dist(cords, vertex_coords) < threshold

#displays a message, atm it just puts it in the center
def display_message(message, font_size):
    text_box_rect = pygame.Rect(250, 50, 700, 100)  # Adjust the size and position as needed
    # Fill the box area with the background color (clearing the area)
    SCREEN.fill((200,200,200), text_box_rect)
    font = pygame.font.Font(None, font_size) 
    text = font.render(message, True, BLACK)  
    text_rect = text.get_rect(center=(600, 100))  
    SCREEN.blit(text, text_rect)
    pygame.display.flip()

#make all verticies one away unbuildable
def make_unbuildable(vertex_coords, board, radius=80):
    """Make all surrounding vertices unbuildable."""
    for vertex in board.vertices.values():
        # Calculate the Euclidean distance from the settlement vertex to each vertex
        distance = math.dist(vertex_coords, vertex.cords)
        # If the distance is less than or equal to the radius, mark it as unbuildable
        if distance <= radius:
            vertex.buildable = False

#helper function for the first roads
def first_road(board, current_player, target_vertex):
    display_message(f"{current_player.name}, please place your road!", 62)
    verts = ADJ_MATRIX[target_vertex]  # Get adjacent vertices
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                for position, vertex in board.vertices.items():
                    
                    if is_close_enough(cords, vertex.cords, threshold=8) and position in verts:

                        current_player.build_road(board,board.vertices[target_vertex],board.vertices[position])
                        print('Road built')
                        
                        return  # Exit the function after building the road

            # Optional: Add a way to cancel road placement (e.g., press ESC)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print('Road placement canceled')
                return

#function for handing out resources
def distribute_rrs(board,roll,players):
    print(roll)
    if roll == 7:
        #do some stuff
        return

    for tile in board.tiles:
        if tile.robber == False and tile.number==roll:
            for vert in tile.verts:
                name = board.vertices[vert].owner
                if name!= None:
                    index = PLAYER_DIC[name]
                    if board.vertices[vert].type=='settlement':
                        #we add 1 
                        if tile.resource not in players[index].resources:
                            players[index].resources[tile.resource] = 1
                            print(name,tile.resource)
                        else:
                            players[index].resources[tile.resource] += 1
                            print(name,tile.resource)

                    elif board.vertices[vert].type=='city':

                        if tile.resource not in players[index].resources:
                            players[index].resources[tile.resource] = 2
                            print(name,tile.resource)
                            print(name,tile.resource)
                        else:
                            players[index].resources[tile.resource] += 2
                            print(name,tile.resource)
                            print(name,tile.resource)
    return

#HUD for players
def draw_sidebar(screen, player, rolled):
    # Draw the sidebar background
    sidebar_rect = pygame.Rect(screen.get_width() - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, screen.get_height())
    pygame.draw.rect(screen, GRAY, sidebar_rect)

    # Define fonts
    font_name = pygame.font.Font(None, 45)
    font = pygame.font.Font(None, 30)

    # Draw the player's name and points
    name_text = font_name.render(f"{player.name}", True, player.color)
    points_text = font.render(f"Points: {player.points}", True, BLACK)
    screen.blit(name_text, (screen.get_width() - SIDEBAR_WIDTH + 10, 15))
    screen.blit(points_text, (screen.get_width() - SIDEBAR_WIDTH + 10, 60))

    # Draw the resources section
    resources_text = font.render("Resources:", True, BLACK)
    screen.blit(resources_text, (screen.get_width() - SIDEBAR_WIDTH + 10, 120))

    y_offset = 150  # Starting y-offset for resources
    for resource, amount in player.resources.items():
        resource_text = font.render(f"{resource}: {amount}", True, BLACK)
        screen.blit(resource_text, (screen.get_width() - SIDEBAR_WIDTH + 10, y_offset))
        y_offset += 30  # Increment y-offset for each resource

    # Draw the buttons section (only if dice has been rolled)
    if rolled:
        # Calculate the starting y-offset for buttons
        button_start_y = 300 + SECTION_SPACING  # Add spacing after resources

        # Define buttons
        buttons = [
            ("Build Road", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, button_start_y),
            ("Build Settlement", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, button_start_y + 60),
            ("Build City", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, button_start_y + 120),
            ("Buy Dev Card", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, button_start_y + 180),
            ("End Turn", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, button_start_y + 240)
        ]

        # Draw buttons
        for text, x, y in buttons:
            button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(screen, player.color, button_rect)
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (x + 10, y + 10))

#main fucntion to control moves
def make_turn(board, turn, players):
    rolled = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if not rolled:
                display_message(f"{players[turn].name}'s turn, press space to roll!", 62)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    roll = rolldice()
                    distribute_rrs(board, roll, players)
                    rolled = True
            else:
                display_message(f"{roll} was rolled", 62)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # Check if a button was clicked
                    if SCREEN.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN <= mouse_pos[0] <= SCREEN.get_width() - BUTTON_MARGIN:
                        button_y_start = 120 + 200  # Starting y position of the first button
                        if button_y_start <= mouse_pos[1] <= button_y_start + BUTTON_HEIGHT:
                            # Build Road
                            print("Build Road clicked")
                            build_road(board,players[turn])


                        elif button_y_start + 60 <= mouse_pos[1] <= button_y_start + 60 + BUTTON_HEIGHT:
                            # Build Settlement
                            print("Build Settlement clicked")
                            build_settlement(board,players[turn])

                        elif button_y_start + 120 <= mouse_pos[1] <= button_y_start + 120 + BUTTON_HEIGHT:
                            # Build City
                            print("Build City clicked")

                        elif button_y_start + 180 <= mouse_pos[1] <= button_y_start + 180 + BUTTON_HEIGHT:
                            # Buy Dev Card
                            print("Buy Dev Card clicked")

                        elif button_y_start + 180 <= mouse_pos[1] <= button_y_start + 240 + BUTTON_HEIGHT:
                            # end turn
                            print("End turn")
                            end_turn(board,turn,players)
                            return True
                            

        # Draw the sidebar
        draw_sidebar(SCREEN, players[turn], rolled)

        # Update the display
        pygame.display.flip()

#ends turn
def end_turn(board,turn,players):
    if turn == 3:
        turn =0
    else:
        turn = turn+1
    make_turn(board, turn, players)

#checks if the vertex is reachable
def reachable(board,player,vertex):
    for edge in board.edges:
        if edge.owner==player.name:
            if vertex == edge.vertex1.id or vertex == edge.vertex2.id:
                return True
    return False

#builds the city
def build_settlement(board,player):
    #add this when we want to purchase
    rrs = ['wheat','sheep','brick','wood']
    for r in rrs:
        if r not in player.resources or player.resources[r]<1:
            print("does not have enough resources")
            return 
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                for id, vertex in board.vertices.items():
                # Calculate the distance between the click and the vertex
                    if is_close_enough(cords, vertex.cords, threshold=8):
                        if vertex.buildable==True and reachable(board,player,vertex):
                            player.build_settlement(board, vertex)  #ent
                            make_unbuildable(cords,board)
                            make_board(SCREEN,board)
                            pygame.display.update() 
                            for r in rrs:
                                player.resources[r] = player.resources[r]-1
                        return
        make_board(board)
        pygame.display.update() 
                                              
#builds the road
def build_road(board,player):
    verts = []
    rrs = ['wood','brick']
    running = True
    for r in rrs:
        if r not in player.resources or player.resources[r]<1:
            print("does not have enough resources")
            return 
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                # Find the vertex closest to the mouse click
                for id, vertex in board.vertices.items():
                    # add the checker
                    if is_close_enough(cords, vertex.cords, threshold=8):
                   
                        if len(verts) == 0:  # First click, record the vertex
                            if reachable(board, player, vertex):
                                verts.append(vertex)
                                print('First vertex reachable:', vertex)
                                break  # Exit the loop after selecting the first vertex
                            else:
                                print("Vertex not reachable.")
                                return  # Return early if the first vertex is not reachable
                        
                        else:  # Second click, check if it's valid
                            if vertex in board.adj_matrix[verts[0]]:  # Check adjacency
                                verts.append(vertex)
                                edge = Edge(board.vertices[verts[0]], board.vertices[verts[1]], player.name)
                                board.edges.append(edge)
                                print(f"Road built between {verts[0]} and {verts[1]}")
                                running = False  # Stop the loop after the second vertex is selected and road is built
                                break  # Exit the loop after building the road
                            else:
                                print("Second vertex is not adjacent.")
                                verts.clear()  # Clear the vertex list to allow retrying
                                break  # Exit to start over with a new selection
        make_board(board)
        pygame.display.update()  # Update the display after processing events

    return
        
# def overseven(players):

#     for player in players:
#         total = sum(player.resources.values())  # Total resources count
        
#         if total >= 8:
#             to_remove = math.floor(total / 2)
#             resources = list(player.resources.keys())
#             count = 0
            
#             while count < to_remove:
            
#                 resource = random.choice(resources)
#                 if resource not in player.resources:
#                     resources.remove(resource)
                
#                 elif player.resources[resource] > 0: 
#                     player.resources[resource] -= 1  
#                     if player.resources[resource] == 0:  
#                         del player.resources[resource]
#                     count += 1 
#                 else:
#                     resources.remove(resource)  

#     return
        
# def rob(board, players, hex_to_verts):
#     turn = board.turn - 1  # Adjust for 0-based index
#     current_player = players[turn]
    
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 return

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 cords = event.pos  # Get the mouse click coordinates
#                 mouse_x, mouse_y = cords

#                 #go over each tile and check if the click is within the hexagon
#                 for tile in board.tiles:
#                     x_center = tile.xcenter
#                     y_center = tile.ycenter

#                     #distance between the mouse click and the center of the tile
#                     distance = math.sqrt((mouse_x - x_center) ** 2 + (mouse_y - y_center) ** 2)

#                     #if the click is within the threshold 
#                     if distance <= HEX_SIZE:
#                         print(f"Clicked on tile at ({mouse_x}, {mouse_y}) with center at ({x_center}, {y_center})")
                        
#                         # Check if the robber is already on the tile
#                         if not hex_to_verts[tile.number]["robber"]:
#                             # Place the robber on this tile
#                             hex_to_verts[tile.number]["robber"] = True
                            
#                             print(f"Robber placed on tile {tile.number}")
#                         else:
#                             print(f"Tile {tile.number} already has the robber.")
                        
#                         #needs to steal from player
                        
#                         return  # Exit after handling the click

#     return

   # def build_city(board, player, vertex_positions):
#     rrs = ['wheat', 'wheat', 'ore', 'ore', 'ore']  # Resources required to build a city

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 cords = event.pos
#                 for position, vertex in vertex_positions.items():
#                     # Calculate the distance between the click and the vertex
#                     distance = math.sqrt((cords[0] - position[0])**2 + (cords[1] - position[1])**2)
#                     if distance <= CLICK_RADIUS:
#                         # Check if the player owns the vertex and has enough resources to build a city
#                         print(player.name)
#                         print(board.vertices[vertex].owner)
#                         if board.vertices[vertex].owner == player.name and board.vertices[vertex].type== "settlement":
#                             # Check if the player has enough resources to build a city
#                             # if player.has_resources(rrs):
#                             player.build_city(board,vertex)  # Call the build_city method
#                             make_board(screen, board)
#                             pygame.display.update() 
#                             print('City built')
#                             return  # Exit after successfully building the city
#                     else:
#                         continue
#                           # Exit if the player does not own the vertex
#                 else:
#                     print('not valid location')
#                     return

#         make_board(screen, board)  # Update the board display
#         pygame.display.update()  # Refresh the screen after each event

# def buy_dev_card(board,player):
#     return True





def main():
    turn = random.randint(0,3)
    setup_phase = True
    main_phase = False
    pygame.init()
    pygame.display.set_caption("Settlers of Catan Board")
    incorrectsetup = True

    while incorrectsetup:
        tiles = create_tiles()
        incorrectsetup = validcheck(tiles)

    hex_cords(tiles)  # Assign coordinates to tiles
    verts, hex_to_verts = create_vertex_for_hex(tiles)
    add_verts_to_each_hex(hex_to_verts,tiles)

    board = Board(tiles,verts)

    #creating players 1 through 4
    PLAYER1 = Player('player1',RED)
    PLAYER2 = Player('player2',GREEN)
    PLAYER3 = Player('player3',BLUE)
    PLAYER4 = Player('player4',ORANGE)

    players = [PLAYER1,PLAYER2,PLAYER3,PLAYER4]

    #Turns for staring, making the settlements etc 
    turns = [0, 1, 2, 3, 3, 2, 1, 0]
    running = True 

    while running:
        make_board(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif setup_phase:
                setup_phase = initialsetup(players, board, turns)
                main_phase = True
            elif main_phase:
                make_turn(board, turn, players)
                turn = (turn + 1) % len(players)

    #for testing
    # PLAYER1.resources = {'wheat':121, 'brick':23, "ore":12,"sheep":12,'wood':23}
    # PLAYER2.resources = {'wheat':4, 'brick':23, "ore":12,"sheep":12,'wood':23}
    # PLAYER3.resources = {'wheat':151, 'brick':23, "ore":12,"sheep":12,'wood':23}
    # PLAYER4.resources = {'wheat':11, 'brick':23, "ore":12,"sheep":12,'wood':23}
    # while running:
    #     make_board(board)
    #     if not main_phase:
    #         make_turn(board,turn,players)


if __name__ == "__main__":
    main()
