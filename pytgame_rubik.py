import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0, 255, 255)

# Initialize pygame
pygame.init()

# Set the width and height of the screen
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Rubik's Cube")


# Loop until the user clicks the close button
done = False
# --- Game logic should go here
# Use to manage how fast the screen updates
clock = pygame.time.Clock()
# --- Drawing code should go here

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    # Draw a color rectangle at the top-left corner of the screen
    i=153
    color = 'RED'
    def printFace(row, columns, color, w=0):
        pygame.draw.rect(screen, color, [row+0, columns+0, 50, 50],width=w)
        pygame.draw.rect(screen, color, [row+51, columns+0, 50, 50],width=w)
        pygame.draw.rect(screen, color, [row+102, columns+0, 50, 50],width=w)
        pygame.draw.rect(screen, color, [row+0, columns+51, 50, 50],width=w)
        pygame.draw.rect(screen, color, [row+51, columns+51, 50, 50],width=w)
        pygame.draw.rect(screen, color, [row+102, columns+51, 50, 50],width=w)
        pygame.draw.rect(screen, color, [row+0, columns+102, 50, 50],width=w)
        pygame.draw.rect(screen, color, [row+51, columns+102, 50, 50],width=w)
        pygame.draw.rect(screen, color, [row+102, columns+102, 50, 50],width=w)
    
    printFace(153,0,'YELLOW')
    printFace(0,154,'BLUE')
    printFace(153,153,'RED')
    printFace(306,153,'GREEN')
    printFace(459,153,'ORANGE')
    printFace(153,306,'BLACK', w=1) # don't fill with border BLACK with width = 1
    
    # Draw a green circle at the center of the screen
    #pygame.draw.circle(screen, GREEN, [350, 250], 100)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
