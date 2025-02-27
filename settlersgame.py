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

DEV_CARDS = ["Knight","Knight","Knight","Knight","Knight","Knight","Knight","Knight","Knight","Knight","Knight","Knight","Knight","Knight","VP","VP","VP","VP","VP","Road Builder","Road Builder","Year of Plenty","Year of Plenty","Monopoly","Monopoly"]
random.shuffle(DEV_CARDS)

#for when a player wins
font_game_over = pygame.font.Font(None, 100)
font_winner = pygame.font.Font(None, 60)

# Confetti settings
CONFETTI_COUNT = 100
confetti = [
    [random.randint(0, WIDTH), random.randint(-HEIGHT, 0), random.choice([RED, YELLOW, BLUE, GREEN])]
    for _ in range(CONFETTI_COUNT)
]

clock = pygame.time.Clock()


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
BUTTON_MARGIN = 10  # Horizontal margin for buttons
BUTTON_SPACING = 25  # Vertical spacing between buttons

DEV_BUTTON_MARGIN = 10
DEV_BUTTON_WIDTH = 230
DEV_BUTTON_HEIGHT = 20
DEV_SECTION_SPACING = 100  # Space between sections

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
                            if current_player.points ==2:
                                for tile in board.tiles:
                                    if vertexid in tile.verts:
                                        if tile.resource!= "Desert":
                                            if tile.resource in current_player.resources:
                                                current_player.resources[tile.resource]+=1
                                            else:
                                                current_player.resources[tile.resource] =1 
                                            
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
def distribute_rrs(board,roll,players,turn):
    print(roll)
    if roll == 7:
        display_message(f"7 rolled! Move the Robber!", 62)
        overseven(players)
        rob(board,players,turn)
        make_board(board)
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
def draw_sidebar(screen, player, rolled,board):
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

    if len(player.rewards) > 0:
        if len(player.rewards)== 1:
            
            font_rew = pygame.font.Font(None, 25)
            rewards_text = font_rew.render(player.rewards[0], True, RED)
            screen.blit(rewards_text, (screen.get_width() - SIDEBAR_WIDTH + 10, 90))
        else:
            font_rew = pygame.font.Font(None, 25)
            rewards_text = font_rew.render(player.rewards[0], True, RED)
            screen.blit(rewards_text, (screen.get_width() - SIDEBAR_WIDTH + 10, 90))
            #for longest road
            font_road = pygame.font.Font(None, 25)
            rewards_text = font_road.render(player.rewards[1], True, BLUE)
            screen.blit(rewards_text, (screen.get_width() - SIDEBAR_WIDTH + 125, 90))
          


    # Draw the resources section
    resources_text = font.render("Resources:", True, BLACK)
    screen.blit(resources_text, (screen.get_width() - SIDEBAR_WIDTH + 10, 120))

    y_offset = 150  # Starting y-offset for resources
    for resource, amount in player.resources.items():
        resource_text = font.render(f"{resource}: {amount}", True, BLACK)
        screen.blit(resource_text, (screen.get_width() - SIDEBAR_WIDTH + 10, y_offset))
        y_offset += 30  # Increment y-offset for each resource
    

    dev_text = font.render("Development Cards:", True, BLACK)
    screen.blit(dev_text, (screen.get_width() - SIDEBAR_WIDTH + 10, 620))

    if player.points >=10:
        board.gameover = True
        board.winner= player
        return

    if rolled:
        # Calculate the starting y-offset for buttons
        button_start_y = 300 + SECTION_SPACING  # Add spacing after resources

        # Define buttons
        buttons = [
            ("Build Road", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, button_start_y),
            ("Build Settlement", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, button_start_y + 60),
            ("Build City", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, button_start_y + 120),
            ("Buy Dev Card", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, button_start_y + 180),
            ("End Turn", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, button_start_y + 240),
        ]   
        
        
        devbuttons = [
                    ("Knight", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, 660),
                    ("Monopoly", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, 660 + BUTTON_SPACING),
                    ("Year of Plenty", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, 660 + 2 * BUTTON_SPACING),
                    ("Road Builder", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, 660 + 3 * BUTTON_SPACING),
                    ("VP", screen.get_width() - SIDEBAR_WIDTH + BUTTON_MARGIN, 660 + 4 * BUTTON_SPACING),
                ]

        # Draw buttons
        for text, x, y in buttons:
            button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(screen, player.color, button_rect)
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (x + 10, y + 10))

        # Render buttons
        for text, x, y in devbuttons:
            if text in player.dev_cards:  # Check if the player has this type of card
                card_count = player.dev_cards[text]  # Get the number of cards
                button_rect = pygame.Rect(x, y, 230, 20)  # Button dimensions
                pygame.draw.rect(screen, BLACK, button_rect)  # Draw button background

                # Render the text with the card count
                button_text = f"{text} ({card_count})"  # Combine text and card count
                text_surface = font.render(button_text, True, WHITE)  # Render the text
                screen.blit(text_surface, (x + 10, y + 2))  # Draw the text on the button

#for the final winner
def draw_game_over_screen(player):
    SCREEN.fill(WHITE)

    # Draw "Game Over!" text
    game_over_text = font_game_over.render("GAME OVER!", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    SCREEN.blit(game_over_text, game_over_rect)

    # Draw winner text
    winner_text = font_winner.render(player.name + " WON!", True, BLUE)
    winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(winner_text, winner_rect)

#when a player wins
def draw_confetti():
    for i in range(len(confetti)):
        x, y, color = confetti[i]
        pygame.draw.circle(SCREEN, color, (x, y), 5)  # Small confetti circles
        confetti[i][1] += random.randint(2, 6)  # Falling speed
        if confetti[i][1] > HEIGHT:  # Reset confetti at top
            confetti[i][0] = random.randint(0, WIDTH)
            confetti[i][1] = random.randint(-HEIGHT, 0)

#main fucntion to control moves
def make_turn(board, turn, players):

    players[turn].playeddev = False
    rolled = False
    for p in players:
        if "Longest Road" in p.rewards and board.haslongestroad!=p.name:
            p.rewards.remove("Longest Road")
            p.points-=2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if not rolled:
                display_message(f"{players[turn].name}'s turn, press space to roll!", 62)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    roll = rolldice()
                    distribute_rrs(board, roll, players,turn)
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
                            build_city(board,players[turn])

                        elif button_y_start + 180 <= mouse_pos[1] <= button_y_start + 180 + BUTTON_HEIGHT:
                            # Buy Dev Card
                            print("Buy Dev Card clicked")
                            buy_dev_card(board,players[turn])

                        elif button_y_start + 240 <= mouse_pos[1] <= button_y_start + 240 + BUTTON_HEIGHT:
                            # end turn
                            print("End turn")
                            end_turn(board,turn,players)
                            return True
                        
                        elif button_y_start + 340 <= mouse_pos[1] <= button_y_start + 340 + DEV_BUTTON_HEIGHT:
                            print("Pressed Knight")
                            useknight(board,players,turn)

                        elif button_y_start + 355 <= mouse_pos[1] <= button_y_start + 360 + DEV_BUTTON_HEIGHT:
                            useMonopoly(board,players[turn],players)
                            print("Pressed Monopoly")
                        
                        elif button_y_start + 385 <= mouse_pos[1] <= button_y_start + 385 + DEV_BUTTON_HEIGHT:
                            useYOP(board,players[turn],players)
                            print("Pressed Year of Plenty")

                        elif button_y_start + 400 <= mouse_pos[1] <= button_y_start + 410 + DEV_BUTTON_HEIGHT:
                            useroadbuilder(board,players[turn],players)
                            print("Road Builder")
        # Draw the sidebar
        if board.gameover == True:
            return
        draw_sidebar(SCREEN, players[turn], rolled,board)
        # Update the display
        pygame.display.flip()

#helper function for monopoly
def stealall(board,current_player,players):
    if current_player.playeddev == True:
        return
    display_message("Click resource tile to steal!", 62)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos  # Get the mouse click coordinates
                mouse_x, mouse_y = cords

                #go over each tile and check if the click is within the hexagon
                for tile in board.tiles:
                    x_center = tile.xcenter
                    y_center = tile.ycenter

                    #distance between the mouse click and the center of the tile
                    distance = math.sqrt((mouse_x - x_center) ** 2 + (mouse_y - y_center) ** 2)

                    #if the click is within the threshold 
                    if distance <= HEX_SIZE:
                        rtype = tile.resource
                        count = 0
                        for player in players:
                            if rtype in player.resources:
                                count += player.resources[rtype]
                                player.resources[rtype] = 0
                        
                        if rtype in current_player.resources:
                            current_player.resources[rtype] += count
                            pygame.display.update()
                            player.playeddev=True
                            return
                        else: 
                            current_player.resources[rtype] = count
                            pygame.display.update()
                            player.playeddev=True
                            return

#using of mon dev card
def useMonopoly(board,current_player,players):
    if current_player.playeddev == True:
        return
    if 'Monopoly' in current_player.dev_cards and current_player.dev_cards["Monopoly"]>=1:
        stealall(board,current_player,players)
        current_player.dev_cards["Monopoly"]-=1
        current_player.playeddev = True
    return True

# helper function for year of plenty 
def take_two(board,current_player):

    display_message("Click 2 resource tiles to steal!", 55)
    types = []
    while len(types)<2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos  # Get the mouse click coordinates
                mouse_x, mouse_y = cords

                #go over each tile and check if the click is within the hexagon
                for tile in board.tiles:
                    x_center = tile.xcenter
                    y_center = tile.ycenter

                    #distance between the mouse click and the center of the tile
                    distance = math.sqrt((mouse_x - x_center) ** 2 + (mouse_y - y_center) ** 2)

                    #if the click is within the threshold 
                    if distance <= HEX_SIZE:
                        rtype = tile.resource
                        types.append(rtype)
    for r in types:
        if r not in current_player.resources:
            current_player.resources[r] = 1
            pygame.display.update()
        else:
            current_player.resources[r] += 1
            pygame.display.update()

#using YOP dev
def useYOP(board,current_player,players):
    if current_player.playeddev == True:
        return
    if 'Year of Plenty' in current_player.dev_cards and current_player.dev_cards["Year of Plenty"]>=1:
        take_two(board,current_player)
        current_player.dev_cards["Year of Plenty"]-=1
        current_player.playeddev = True
    #check which two resources wnated 
    return True

#use of road builder dev
def useroadbuilder(board,current_player,players):
    if current_player.playeddev == True:
        return
    if 'Road Builder' in current_player.dev_cards and current_player.dev_cards["Road Builder"]>=1:
        freeroads(board,current_player)
        current_player.dev_cards["Road Builder"]-=1
        current_player.playeddev = True

#use of knight dev 
def useknight(board,players,turn):

    if players[turn].playeddev == True:
        print("true")
        return
    
    elif 'Knight' in players[turn].dev_cards and players[turn].dev_cards["Knight"]>=1:
        players[turn].playeddev = True
        display_message("Move the Knight!", 62)
        rob(board,players,turn)
        players[turn].dev_cards["Knight"]-=1
        players[turn].knightsplayed +=1 
        #case of first person to make it to 3 knights 
        if players[turn].knightsplayed >= board.knightsneeded:
            if board.largestarmy==None:
                board.largestarmy = players[turn]
                players[turn].points+=2 
                board.knightsneeded +=1 
                players[turn].rewards.append("Largest Army")
            elif players[turn].name == board.largestarmy.name:
                board.knightsneeded +=1
            else:
                board.largestarmy.points-=2
                board.largestarmy.rewards.remove("Largest Army")
                board.largestarmy = players[turn]
                players[turn].points+=2 
                players[turn].rewards.append("Largest Army")
                board.knightsneeded +=1 
        make_board(board)

    return True
    #chekc if we have a card because it is clickable whenever

#ends turn
def end_turn(board,turn,players):
    if players[turn].points >=10:
        return
        #exit the game loop
    if turn == 3:
        turn =0
    else:
        turn = turn+1
    make_turn(board, turn, players)

#checks if the vertex is reachable, need to fix it so cannot build over top of an edge
def reachable(board,player,vertex):
    
    for edge in board.edges:
        if edge.owner==player.name:
            if vertex.id == edge.vertex1.id or vertex.id == edge.vertex2.id:
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
                            player.build_settlement(board, id)  #ent
                            make_unbuildable(cords,board)
                            make_board(board)
                            pygame.display.update() 
                            for r in rrs:
                                player.resources[r]-=1
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
                            if vertex.owner == None or vertex.owner==player.name:
                                if reachable(board, player, vertex):
                                    verts.append(vertex.id)
                                    print('First vertex reachable:', vertex)
                                    break  #Exit the loop after selecting the first vertex
                                else:
                                    print("Vertex not reachable.")
                                    return  # Return early if the first vertex is not reachable
                            return
                            
                        else:  #Second click, check if it's valid
                            if vertex.id in ADJ_MATRIX[verts[0]]:  #Check adjacency
                                verts.append(vertex.id)
                                #catches roads already built
                                for edge in board.edges:
                                    # print(edge.vertex1.id,edge.vertex2)
                                    # print(verts[0],verts[1])
                                    if (edge.vertex1.id==verts[0] and edge.vertex2.id==verts[1]) or (edge.vertex1.id==verts[1] and edge.vertex2.id==verts[0]):
                                        print("vert already in")
                                        return
                                
                                edge = Edge(board.vertices[verts[0]], board.vertices[verts[1]], player.name,player.color)
                                board.edges.append(edge)
                                for r in rrs:
                                    player.resources[r]-=1
                                print(f"Road built between {verts[0]} and {verts[1]}")
                                longest = get_longest_road(board,player)
                                if longest>board.longestroad:
                                    board.haslongestroad = player.name
                                    board.longestroard = longest
                                    if "Longest Road" not in player.rewards:
                                        player.rewards.append("Longest Road")
                                        player.points+=2
                                running = False  
                                break  
                            else:
                                print("Second vertex is not adjacent.")
                                verts.clear()  
                                break  
        make_board(board)
        pygame.display.update()  
        

    return

#builds a city
def build_city(board, player):

    rrs = ['wheat', 'wheat', 'ore', 'ore', 'ore']  # Resources required to build a city
    if 'wheat' not in player.resources or 'ore' not in player.resources:
        return
        
    if player.resources['wheat']<2 or player.resources['ore']<3:
        print('player does not have rrs')
        return 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                for id, vertex in board.vertices.items():
                    # Calculate the distance between the click and the vertex
                    if is_close_enough(cords, vertex.cords, threshold=8):
                        # Check if the player owns the vertex and has enough resources to build a city
                        if board.vertices[id].owner == player.name and board.vertices[id].type== "settlement":
                            player.build_city(board,id)  # Call the build_city method
                            make_board(board)
                            pygame.display.update() 
                            for r in rrs:
                                player.resources[r]-= 1
                            print('City built')
                            return  
                    else:
                        continue
                          #Exit if the player does not own the vertex
                else:
                    print('not valid location')
                    return

        make_board(board)  # Update the board display
        pygame.display.update()  # Refresh the screen after each event

#randomly removes half if over 7
def overseven(players):
    for player in players:
        total = sum(player.resources.values())  # Total resources count
        if total >= 8:
            to_remove = math.floor(total / 2)
            resources = list(player.resources.keys())
            count = 0
            while count < to_remove:
                resource = random.choice(resources)
                if resource not in player.resources:
                    resources.remove(resource)
                
                elif player.resources[resource] > 0: 
                    player.resources[resource] -= 1  
                    if player.resources[resource] == 0:  
                        del player.resources[resource]
                    count += 1 
                else:
                    resources.remove(resource)  
    pygame.display.update() 
    return

#randomly takes a card 
def rob(board,players,turn):
    current_player = players[turn]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos  # Get the mouse click coordinates
                mouse_x, mouse_y = cords

                #go over each tile and check if the click is within the hexagon
                for tile in board.tiles:
                    x_center = tile.xcenter
                    y_center = tile.ycenter

                    #distance between the mouse click and the center of the tile
                    distance = math.sqrt((mouse_x - x_center) ** 2 + (mouse_y - y_center) ** 2)

                    #if the click is within the threshold 
                    if distance <= HEX_SIZE:
                        print(f"Clicked on tile at ({mouse_x}, {mouse_y}) with center at ({x_center}, {y_center})")
                        
                        # Check if the robber is already on the tile
                        if tile.robber == False:
                            # Place the robber on this tile
                            tile.robber = True
                            current_robbed = tile.id 
                            print(f"Robber placed on tile {tile.number}")
                            stealable_players= []
                            for vert in tile.verts:
                                if board.vertices[vert].owner!= None:
                                    stealable_players.append(vert)
                            choose_to_steal(current_player,stealable_players,players,board)

                            #needs to steal from player
                            #removes the robber from the other tiles
                            for tile in board.tiles:
                                if tile.robber == True and tile.id != current_robbed:
                                    tile.robber = False
                                
                            return 
                        else:
                            print(f"Tile {tile.number} already has the robber.")
                        
                         
    return

#fucntion allows user to select who to steal card from
def choose_to_steal(current_player,stealable_players,players,board):
    if len(stealable_players) == 0:
        return
    display_message(f"Choose a player to steal from. Click their settlment",62)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                for position, vertex in board.vertices.items():
                    if is_close_enough(cords, vertex.cords, threshold=8) and position in stealable_players:
                        steal_name = board.vertices[position].owner
                        steal_choices = []
                        for player in players:
                            if player.name == steal_name:
                                temp = player
                                for rrs in player.resources:
                                    if player.resources[rrs] >0:
                                        steal_choices.append(rrs)
                        if len(steal_choices)== 0: 
                            return  
                        else:
                            r = random.choice(steal_choices)
                            temp.resources[r]-=1
                            if r in current_player.resources:
                                current_player.resources[r]+=1
                                print(current_player.name,r)
                                return
                            else:
                                current_player.resources[r]=1
                                print(current_player.name,r)
                                return
                                    
#funciton to process buying of dev cards
def buy_dev_card(board,player):
    rrs = ["wheat","sheep","ore"]
    if 'wheat' not in player.resources or 'ore' not in player.resources or "sheep" not in player.resources:
        print("not enough resources")
        return
    
    if player.resources['wheat']<1 or player.resources['ore']<1 or player.resources['sheep']<1:
        print('player does not have rrs')
        return 
    
    if len(DEV_CARDS) == 0:
        print("no dev cards left")
        return
   
    else:
        #player can afford
        player.playeddev= True
        card = DEV_CARDS.pop()
        if card not in player.dev_cards:
            player.dev_cards[card] = 1
        else:
            player.dev_cards[card] += 1
        if card == "VP":
            player.points+=1
        for r in rrs:
            player.resources[r]-=1

        
        make_board(board)
        pygame.display.update() 

#function for road building dev card
def freeroads(board,player):
    display_message("Place 2 free roads!", 62)
    verts = []
    count =0
    while count<2:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                # Find the vertex closest to the mouse click
                for id, vertex in board.vertices.items():
                    # add the checker
                    if is_close_enough(cords, vertex.cords, threshold=8):
                        if len(verts) == 0:  # First click, record the vertex
                            if reachable(board, player, vertex):
                                verts.append(vertex.id)
                                print('First vertex reachable:', vertex)
                                break  #Exit the loop after selecting the first vertex
                            else:
                                print("Vertex not reachable.")
                                return  # Return early if the first vertex is not reachable
                            
                        else:  #Second click, check if it's valid
                            if vertex.id in ADJ_MATRIX[verts[0]]:  #Check adjacency
                                verts.append(vertex.id)
                                edge = Edge(board.vertices[verts[0]], board.vertices[verts[1]], player.name,player.color)
                                board.edges.append(edge)
                                count +=1 
                                break  
                            else:
                                print("Second vertex is not adjacent.")
                                verts.clear()  
                                break  
        make_board(board)
        pygame.display.update()  

    return


#function to find longeset road
def get_longest_road(board, player):
    # Step 1: Filter only roads owned by the player
    player_roads = {(edge.vertex1.id, edge.vertex2.id) for edge in board.edges if edge.owner == player.name}

    # Step 2: Build an adjacency list for the player's roads
    road_graph = {v: set() for v1, v2 in player_roads for v in (v1, v2)}
    for v1, v2 in player_roads:
        road_graph[v1].add(v2)
        road_graph[v2].add(v1)

    # Step 3: DFS function to find the longest path
    def dfs(vertex, visited_edges):
        max_length = 0
        for neighbor in road_graph[vertex]:
            edge = tuple(sorted((vertex, neighbor)))
            if edge not in visited_edges:
                visited_edges.add(edge)
                max_length = max(max_length, 1 + dfs(neighbor, visited_edges))
                visited_edges.remove(edge)
        return max_length

    # Step 4: Run DFS from all road endpoints
    longest_road = 0
    for v1, v2 in player_roads:
        longest_road = max(longest_road, dfs(v1, {tuple(sorted((v1, v2)))}))
        longest_road = max(longest_road, dfs(v2, {tuple(sorted((v1, v2)))}))
    return longest_road  # Ensure function returns a value


#main function 
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
    # running = True 
    
    while board.gameover==False:
        make_board(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.gameover = True
            elif setup_phase:
                setup_phase = initialsetup(players, board, turns)
                main_phase = True
            elif main_phase:
                make_turn(board, turn, players)
                turn = (turn + 1) % len(players)
    
    print("game over")
    while True:
        SCREEN.fill(WHITE)
        draw_game_over_screen(board.winner)
        draw_confetti()

        pygame.display.flip()  # Refresh the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  



if __name__ == "__main__":
    main()

#need to add ports


# A couple notes: when a 7 is rolled, you do not get to choose which cards you remove, it is random...
# 2. there is an issue where if you make an error while using the road builder, it will cancel it.
# 3. trading is not available atm 
# 4. there is no limit on resources, or a limit to roads/houses/cities
# 5. dev cards, must be played before buying new ones, otherwise will not work
# 6. need ports still 
