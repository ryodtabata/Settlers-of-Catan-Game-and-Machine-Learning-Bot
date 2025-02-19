# Example HexTile Class
import random
import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

#each hextile on the game board
class HexTile:
    def __init__(self, resource, number, id):
        self.resource = resource
        self.number = number
        self.robber = False
        self.xcenter = None
        self.ycenter= None
        self.verts= None
        self.id = id

# each hex has list of verticies, each vertex has a onwer, and type
class Vertex:
    def __init__(self,id,cords):
        self.id = id
        self.owner = None 
        self.type = None #city or settlement 
        self.cords = cords
        self.buildable = True
        self.color = None

#roads, owner, id, and its verts 
class Edge:
    def __init__(self,vertex1,vertex2,owner,color):
        self.id = id
        self.owner = owner
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.color = color

class Board():
    def __init__(self,tiles,vertices):
        self.tiles = tiles
        self.edges = []
        self.turn = random.randint(1,4)
        self.vertices = vertices
        self.longestroad = None
        self.largestarmy = None
             
class Player():
    def __init__(self,name,color):
        self.resources = {}
        self.points = 0
        self.dev_cards = {}
        self.rewards = [] #longest road, largest army
        self.name = name
        self.color = color
        self.knightsplayed = 0
    
    def build_settlement(self,board,vertex):
        board.vertices[vertex].owner = self.name
        board.vertices[vertex].type = "settlement"
        self.points = self.points+1
        board.vertices[vertex].buildable = False
        board.vertices[vertex].color = self.color

    def build_city(self,board,vertex):
        board.vertices[vertex].owner = self.name
        board.vertices[vertex].type = "city"
        board.vertices[vertex].buildable = False
        board.vertices[vertex].color = self.color
        self.points = self.points+1    
    
    def build_road(self,board,vertex1,vertex2):
        edge = Edge(vertex1,vertex2,self.name,self.color)
        board.edges.append(edge)
    

    



