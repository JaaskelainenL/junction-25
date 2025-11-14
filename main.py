import pygame
import sys
from game import Game


game = Game()






# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Input Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 32)
input_font = pygame.font.Font(None, 28)

# Text Input
input_box = pygame.Rect(100, 200, 300, 40)
text = ""
active = False

# Function to render text
def render_text(text, font, color, pos):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle input box events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    text = ""
                    pass  # Do nothing on return key (or you could process the text here)
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    # Draw the input box
    pygame.draw.rect(screen, BLACK, input_box, 2)
    pygame.draw.rect(screen, GRAY, input_box.inflate(-2, -2))  # Inner fill

    # Render the inputted text
    render_text(text, input_font, BLACK, (input_box.x + 5, input_box.y + 5))

    # Display the input text above the box
    render_text("You typed: " + text, font, BLACK, (input_box.x, input_box.y - 40))

    pygame.display.flip()

pygame.quit()
sys.exit()
