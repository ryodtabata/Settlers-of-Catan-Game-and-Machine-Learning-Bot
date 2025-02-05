# Example HexTile Class
import random
import networkx as nx
import matplotlib.pyplot as plt
import pygame


class HexTile:
    def __init__(self, resource, number):
        self.resource = resource
        self.number = number
        self.robber = False
        self.xcenter = None
        self.ycenter= None
        self.edges = None

# each hex has list of verticies, each vertex has a onwer, and type
class Vertex:
    def __init__(self,id,cords):
        self.id = id
        self.owner = None 
        self.type = None #city or settlement 
        self.cords = cords
        self.buildable = True

class Edge:
    def __init__(self,vertex1,vertex2,owner):
        self.id = id
        self.owner = owner
        self.vertex1 = vertex1
        self.vertex2 = vertex2


class Board():
    def __init__(self,tiles,vertices):
        self.tiles = tiles
        self.edges = []
        self.turn = random.randint(1,4)
        self.vertices = vertices
        self.setupstage = True
        self.maingame = False 
        self.longest_road = None
        self.largest_army = None
        self.adj_matrix = {
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
        
        
class Player():
    def __init__(self,name):
        self.resources = {}
        self.points = 0
        self.dev_cards = {}
        self.rewards = [] #longest road, largest army
        self.roads = [] #keep track of owned roads, to attach
        self.name = name
    
    def build_settlement(self,board,vertex):
        board.vertices[vertex].owner = self.name
        board.vertices[vertex].type = "settlement"
        self.points = self.points+1
        board.vertices[vertex].buildable = False

    def build_city(self,board,vertex):
        board.vertices[vertex].owner = self.name
        board.vertices[vertex].type = "city"
        self.points = self.points+1    
    

    
   

# Button class to simplify button handling
class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
        self.font = pygame.font.Font(None, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)