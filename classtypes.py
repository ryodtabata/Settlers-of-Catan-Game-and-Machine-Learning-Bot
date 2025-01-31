# Example HexTile Class
import random

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
    
    def build_road(self,board,vertex1,vertex2):
        edge = Edge(vertex1,vertex2)
        board.edges.append(edge)
        return edge

    
   
