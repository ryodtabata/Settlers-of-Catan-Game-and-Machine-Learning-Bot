import pygame
from classtypes import *
from settlersgame import *


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)

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

def maketurn(board, players, screen,vertex_positions):
    """
    Handles a player's turn in Pygame.
    """
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
        Button(50, 300, 200, 50, "Build Road", (0, 128, 255), lambda: add_road(board, current_player,vertex_positions)),
        Button(50, 360, 200, 50, "Build Settlement", (0, 128, 0), lambda: build_settlement(board, current_player)),
        Button(50, 420, 200, 50, "Build City", (255, 165, 0), lambda: build_city(board, current_player)),
        Button(50, 480, 200, 50, "Buy Dev Card", (128, 0, 128), lambda: buy_dev_card(board, current_player)),
        Button(50, 540, 200, 50, "End Turn", (255, 0, 0), lambda: end_turn(board))
    ]

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()

    # Wait for button clicks
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
                        return  # Exit turn UI loop



def build_settlement(board,player):
    return True

def build_city(board,player):
    return True

def buy_dev_card(board,player):
    return True

def end_turn(board):
    if board.turn==4:
        board.turn=1
    else:
        board.turn +=1 
    return True