import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Triangle vertices (x, y coordinates) - starting as a triangle
player = [(300, 100), (250, 200), (350, 200)]

# Speed of movement
speed = 0.1

# Rotation speed
rotation_speed = 5  # degrees per frame

# Function to rotate a point around a given center
def rotate_point(point, angle, center):
    angle_rad = math.radians(angle)
    x, y = point
    cx, cy = center
    new_x = (x - cx) * math.cos(angle_rad) - (y - cy) * math.sin(angle_rad) + cx
    new_y = (x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad) + cy
    return new_x, new_y

# Function to find the center of the triangle
def find_center(points):
    x_coords = [x for x, y in points]
    y_coords = [y for x, y in points]
    return sum(x_coords) / len(points), sum(y_coords) / len(points)

run = True
angle = 0

while run:
    screen.fill((0, 0, 0))  # Fill screen with black

    # Find the center of the triangle
    center = find_center(player)

    # Rotate the triangle
    rotated_player = [rotate_point(p, angle, center) for p in player]
    angle += rotation_speed

    # Draw the rotated red triangle
    pygame.draw.polygon(screen, (255, 0, 0), rotated_player)

    # Handle movement
    key = pygame.key.get_pressed()

    if key[pygame.K_a]:  # Move left
        player = [(x - speed, y) for x, y in player]
    if key[pygame.K_d]:  # Move right
        player = [(x + speed, y) for x, y in player]
    if key[pygame.K_w]:  # Move up
        player = [(x, y - speed) for x, y in player]
    if key[pygame.K_s]:  # Move down
        player = [(x, y + speed) for x, y in player]

    # Event handling to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()