# Example HexTile Class
import random
import pygame

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
        board.verteces[vertex].color = self.color
        self.points = self.points+1    
    
    def build_road(self,board,vertex1,vertex2):
        edge = Edge(vertex1,vertex2,self.name,self.color)
        board.edges.append(edge)
    
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